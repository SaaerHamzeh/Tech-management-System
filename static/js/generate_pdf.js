
function generatePDF() {
    const searchParams = new URLSearchParams(new FormData(document.querySelector('form')))
    window.location.href = "{% url 'generate_pdf' %}?" + searchParams.toString()
}
