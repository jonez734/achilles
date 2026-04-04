$(document).ready(function() {
    $('.section .header h1').on('click', function() {
        var $header = $(this);
        var $section = $header.closest('.section');
        var $body = $section.find('.body'); // The placeholder .body in section.tmpl
        var sectionName = $section.data('name');

        if ($.trim($body.html()) !== '') {
            $body.slideToggle();
        } 
        else {
            $.ajax({
                url: '/achilles/section.php',
                type: 'GET',
                data: { name: sectionName },
                success: function(data) {
                    var $html = $('<div>').html(data);
                    
                    // 1. Swap Header Text
                    var newTitle = $html.find('.header h1').text();
                    if (newTitle) {
                        $header.text(newTitle);
                    }

                    // 2. Extract only the inner content of the loaded .body
                    // This prevents "body inside a body" nesting
                    var newBodyContent = $html.find('.body').html();
                    
                    if (newBodyContent) {
                        $body.html(newBodyContent);
                    } else {
                        // Fallback: if the template doesn't have a .body, use the whole response
                        console.log("fallback");
                        $body.html(data);
                    }

                    $body.hide().slideDown();
                },
                error: function() {
                    $body.html('<div class="error">Error loading section content.</div>').slideDown();
                }
            });
        }
    });

//    $(document).on('click', '.section .body', function() {
//        $(this).slideUp();
//    });
});
