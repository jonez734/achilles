document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".section").forEach(section => {
        const header = section.querySelector(".section-header");
        const content = section.querySelector(".section-content");
        const name = section.dataset.name;

        // Validate section name
        if (!name || !/^[a-zA-Z0-9_-]+$/.test(name)) {
            console.error("Invalid section name");
            return;
        }

        let loaded = false;

        header.addEventListener("click", async () => {
            if (!loaded) {
                try {
                    const response = await fetch(`section.php?name=${encodeURIComponent(name)}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error: ${response.status}`);
                    }
                    const html = await response.text();
                    content.innerHTML = html;
                    loaded = true;
                } catch (err) {
                    content.innerHTML = '<div class="error">Error loading section. Please try again.</div>';
                    console.error("Failed to load section:", err);
                    return;
                }
            }

            content.style.display =
                content.style.display === "none" ? "block" : "none";
        });

        if (section.dataset.open === "1") {
            header.click();
        }
    });
});
