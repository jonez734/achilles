// skin/js/achilles-sections.js
$(document).ready(function() {
    $('.section-header').on('click', function() {
        var $section = $(this).closest('.section');
        var $content = $section.find('.section-content');
        var sectionName = $section.data('name');

        // Toggle visibility with a slide effect
        $content.slideToggle();

        // Only fetch if the container is currently empty
        if ($content.is(':empty')) {
            $content.html('<div class="loading">Loading...</div>');
            
            $.ajax({
                url: 'section.php',
                type: 'GET',
                data: { name: sectionName },
                success: function(data) {
                    $content.html(data);
                },
                error: function() {
                    $content.html('<div class="error">Failed to load content.</div>');
                }
            });
        }
    });
});
