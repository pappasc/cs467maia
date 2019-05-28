# postgresql/pygresql.py
# Copyright (C) 2005-2019 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
"""
.. dialect:: postgresql+pygresql
    :name: pygresql
    :dbapi: pgdb
    :connectstring: postgresql+pygresql://user:password@host:port/dbname[?key=value&key=value...]
    :url: http://www.pygresql.org/
"""  # noqa

import decimal
import re

from .base import _DECIMAL_TYPES
from .base import _FLOAT_TYPES
from .base import _INT_TYPES
from .base import PGCompiler
from .base import PGDialect
from .base import PGIdentifierPreparer
from .base import UUID
from .hstore import HSTORE
from .json import JSON
from .json import JSONB
from ... import exc
from ... import processors
from ... import util
from ...sql.elements import Null
from ...types import JSON as Json
from ...types import Numeric


class _PGNumeric(Numeric):
    def bind_processor(self, dialect):
        return None

    def result_processor(self, dialect, coltype):
        if not isinstance(coltype, int):
            coltype = coltype.oid
        if self.asdecimal:
            if coltype in _FLOAT_TYPES:
                return processors.to_decimal_processor_factory(
                    decimal.Decimal, self._effective_decimal_return_scale
                )
            elif coltype in _DECIMAL_TYPES or coltype in _INT_TYPES:
                # PyGreSQL returns Decimal natively for 1700 (numeric)
                return None
            else:
                raise exc.InvalidRequestError(
                    "Unknown PG numeric type: %d" % coltype
                )
        else:
            if coltype in _FLOAT_TYPES:
                # PyGreSQL returns float natively for 701 (float8)
                return None
            elif coltype in _DECIMAL_TYPES or coltype in _INT_TYPES:
                return processors.to_float
            else:
                raise exc.InvalidRequestError(
                    "Unknown PG numeric type: %d" % coltype
                )


class _PGHStore(HSTORE):
    def bind_processor(self, dialect):
        if not dialect.has_native_hstore:
            return super(_PGHStore, self).bind_processor(dialect)
        hstore = dialect.dbapi.Hstore

        def process(value):
            if isinstance(value, dict):
                return hstore(value)
            return value

        return process

    def result_processor(self, dialect, coltype):
        if not dialect.has_native_hstore:
            return super(_PGHStore, self).result_processor(dialect, coltype)


class _PGJSON(JSON):
    def bind_processor(self, dialect):
        if not dialect.has_native_json:
            return super(_PGJSON, self).bind_processor(dialect)
        json = dialect.dbapi.Json

        def process(value):
            if value is self.NULL:
                value = None
            elif isinstance(value, Null) or (
                value is None and self.none_as_null
            ):
                return None
            if value is None or isinstance(value, (dict, list)):
                return json(value)
            return value

        return process

    def result_processor(self, dialect, coltype):
        if not dialect.has_native_json:
            return super(_PGJSON, self).result_processor(dialect, coltype)


class _PGJSONB(JSONB):
    def bind_processor(self, dialect):
        if not dialect.has_native_json:
            return super(_PGJSONB, self).bind_processor(dialect)
        json = dialect.dbapi.Json

        def process(value):
            if value is self.NULL:
                value = None
            elif isinstance(value, Null) or (
                value is None and self.none_as_null
            ):
                return None
            if value is None or isinstance(value, (dict, list)):
                return json(value)
            return value

        return process

    def result_processor(self, dialect, coltype):
        if not dialect.has_native_json:
            return super(_PGJSONB, self).result_processor(dialect, coltype)


class _PGUUID(UUID):
    def bind_processor(self, dialect):
        if not dialect.has_native_uuid:
            return super(_PGUUID, self).bind_processor(dialect)
        uuid = dialect.dbapi.Uuid

        def process(value):
            if value is None:
                return None
            if isinstance(value, (str, bytes)):
                if len(value) == 16:
                    return uuid(bytes=value)
                return uuid(value)
            if isinstance(value, int):
                return uuid(int=value)
            return value

        return process

    def result_processor(self, dialect, coltype):
        if not dialect.has_native_uuid:
            return super(_PGUUID, self).result_processor(dialect, coltype)
        if not self.as_uuid:

            def process(value):
                if value is not None:
                    return str(value)

            return process


class _PGCompiler(PGCompiler):
    def visit_mod_binary(self, binary, operator, **kw):
        return (
            self.process(binary.left, **kw)
            + " %% "
            + self.process(binary.right, **kw)
        )

    def post_process_text(self, text):
        return text.replace("%", "%%")


class _PGIdentifierPreparer(PGIdentifierPreparer):
    def _escape_identifier(self, value):
        value = value.replace(self.escape_quote, self.escape_to_quote)
        return value.replace("%", "%%")


class PGDialect_pygresql(PGDialect):

    driver = "pygresql"

    statement_compiler = _PGCompiler
    preparer = _PGIdentifierPreparer

    @classmethod
    def dbapi(cls):
        import pgdb

        return pgdb

    colspecs = util.update_copy(
        PGDialect.colspecs,
        {
            Numeric: _PGNumeric,
            HSTORE: _PGHStore,
            Json: _PGJSON,
            JSON: _PGJSON,
            JSONB: _PGJSONB,
            UUID: _PGUUID,
        },
    )

    def __init__(self, **kwargs):
        super(PGDialect_pygresql, self).__init__(**kwargs)
        try:
            version = self.dbapi.version
            m = re.match(r"(\d+)\.(\d+)", version)
            version = (int(m.group(1)), int(m.group(2)))
        except (AttributeError, ValueError, TypeError):
            version = (0, 0)
        self.dbapi_version = version
        if version < (5, 0):
            has_native_hstore = has_native_json = has_native_uuid = False
            if version != (0, 0):
                util.warn(
                    "PyGreSQL is only fully supported by SQLAlchemy"
                    " since version 5.0."
                )
        else:
            self.supports_unicode_statements = True
            self.supports_unicode_binds = True
            has_native_hstore = has_native_json = has_native_uuid = True
        self.has_native_hstore = has_native_hstore
        self.has_native_json = has_native_json
        self.has_native_uuid = has_native_uuid

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user")
        if "port" in opts:
            opts["host"] = "%s:%s" % (
                opts.get("host", "").rsplit(":", 1)[0],
                opts.pop("port"),
            )
        opts.update(url.query)
        return [], opts

    def is_disconnect(self, e, connection, cursor):
        if isinstance(e, self.dbapi.Error):
            if not connection:
                return False
            try:
                connection = connection.connection
            except AttributeError:
                pass
            else:
                if not connection:
                    return False
            try:
                return connection.closed
            except AttributeError:  # PyGreSQL < 5.0
                return connection._cnx is None
        return False


dialect = PGDialect_pygresql
