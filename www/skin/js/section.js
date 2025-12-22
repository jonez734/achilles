$(document).ready(function() {
    $('.section-header').on('click', function() {
        var $section = $(this).closest('.section');
        var $content = $section.find('.section-content');
        var sectionName = $section.data('name');

        // CASE 1: Content is already there (either open or previously loaded)
        if ($.trim($content.html()) !== '') {
            console.log("Toggling existing content for: " + sectionName);
            $content.slideToggle(); // This handles the "close" if it's currently open
        } 
        // CASE 2: Content is empty (first time click)
        else {
            console.log("First load for: " + sectionName);
            
            $.ajax({
                url: '/achilles/section.php',
                type: 'GET',
                data: { name: sectionName },
                success: function(data) {
                    $content.html(data);
                    // Hide immediately so slideDown has a starting point of 0 height
                    $content.hide().slideDown(); 
                },
                error: function() {
                    $content.html('<div class="error">Error loading content.</div>').slideDown();
                }
            });
        }
    });
});
