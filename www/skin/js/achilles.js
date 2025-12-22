document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".section").forEach(section => {
        const header = section.querySelector(".section-header");
        const content = section.querySelector(".section-content");
        const name = section.dataset.name;

        let loaded = false;

        header.addEventListener("click", async () => {
            if (!loaded) {
                const html = await fetch(`section.php?name=${encodeURIComponent(name)}`)
                    .then(r => r.text());

                content.innerHTML = html;
                loaded = true;
            }

            // toggle
            content.style.display =
                content.style.display === "none" ? "block" : "none";
        });

        // Auto-open if editor set "open: true"
        if (section.dataset.open === "1") {
            header.click();
        }
    });
});
