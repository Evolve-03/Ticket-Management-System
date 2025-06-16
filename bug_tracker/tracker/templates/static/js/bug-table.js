document.addEventListener("DOMContentLoaded", function () {
    const table = document.querySelector("#ticketTable tbody");
    const rows = Array.from(table.rows);
    const rowsPerBatch = 6;
    let currentIndex = 6;

    rows.forEach(row => row.style.display = "none");
    rows.slice(0, currentIndex).forEach(row => row.style.display = "");

    const container = document.querySelector(".table-container");
    container.addEventListener("scroll", function () {
        if (container.scrollTop + container.clientHeight >= container.scrollHeight - 5) {
            const nextRows = rows.slice(currentIndex, currentIndex + rowsPerBatch);
            nextRows.forEach(row => row.style.display = "");
            currentIndex += rowsPerBatch;
        }
    });
});
