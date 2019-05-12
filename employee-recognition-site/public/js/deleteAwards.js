function deleteAwards(id){
    $.ajax({
        url: '/awards/' + id,
        type: 'DELETE',
        success: function(result){
            window.location.reload(true);
        }
    })
};
