$(document).ready(function() {
    $('.fa-heart').on('click', function() {
        $(this).toggleClass('text-muted text-danger');
    });

    $('.card-produto .card-body').on('click', function() {
        window.location.href = 'produto.html';
    })
});