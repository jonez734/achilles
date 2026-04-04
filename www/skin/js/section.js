$(document).ready(function() {
    $('.section .header h1').on('click', function() {
        var $header = $(this);
        var $section = $header.closest('.section');
        var $body = $section.find('.body');
        var sectionName = $section.data('name');

        // Validate section name - only allow alphanumeric, hyphens, underscores
        if (!sectionName || !/^[a-zA-Z0-9_-]+$/.test(sectionName)) {
            $body.html('<div class="error">Invalid section.</div>').slideDown();
            return;
        }

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
                    
                    var newTitle = $html.find('.header h1').text();
                    if (newTitle && newTitle.trim()) {
                        $header.text(newTitle.trim());
                    }

                    var newBodyContent = $html.find('.body').html();
                    
                    if (newBodyContent) {
                        $body.html(newBodyContent);
                    } else {
                        $body.html(data);
                    }

                    $body.hide().slideDown();
                },
                error: function(xhr, status, error) {
                    $body.html('<div class="error">Error loading section. Please try again.</div>').slideDown();
                }
            });
        }
    });
});
