class CustomSVG extends HTMLElement {
    async connectedCallback() {
        const src = this.getAttribute('src');
        const classes = this.getAttribute('class') || '';

        if (src) {
            try {
                const response = await fetch(src);
                const svgText = await response.text();
                const svgElement = new DOMParser().parseFromString(svgText, 'image/svg+xml').querySelector('svg');

                if (svgElement) {
                    svgElement.setAttribute('class', classes);
                    this.appendChild(svgElement);
                }
            } catch (error) {
                console.error('Error loading SVG:', error);
            }
        }
    }
}

customElements.define('custom-svg', CustomSVG);