document.addEventListener('DOMContentLoaded', function() {
    // Form submission with loading indicator
    const form = document.querySelector('form');
    const button = document.querySelector('.search-button');
    const buttonText = button.querySelector('.button-text');
    const buttonIcon = button.querySelector('.button-icon');
    
    if (form) {
        form.addEventListener('submit', function() {
            // Create loading indicator if it doesn't exist
            if (!document.querySelector('.loading-indicator')) {
                const loadingIndicator = document.createElement('span');
                loadingIndicator.className = 'loading-indicator';
                buttonIcon.innerHTML = '';
                buttonIcon.appendChild(loadingIndicator);
            }
            
            buttonText.textContent = 'Thinking...';
            button.disabled = true;
        });
    }
    
    // Make example items clickable on the main page
    const mainExampleItems = document.querySelectorAll('.examples-section .example-item');
    mainExampleItems.forEach(item => {
        item.addEventListener('click', function() {
            const questionText = this.textContent.replace(/^[\s\u00A0•]+|[\s\u00A0•]+$/g, '');
            document.querySelector('.search-input').value = questionText;
            
            // Optional: Auto-submit the form
            // form.submit();
        });
    });
    
    // Handle prefill parameter from URL if present
    const urlParams = new URLSearchParams(window.location.search);
    const prefill = urlParams.get('prefill');
    if (prefill) {
        const searchInput = document.querySelector('.search-input');
        if (searchInput && !searchInput.value) {
            searchInput.value = prefill;
            // Optional: Auto-submit form when coming from examples
            // form.submit();
        }
    }
    
    // Format the answer text for better display
    const answerElement = document.querySelector('.answer');
    if (answerElement) {
        let content = answerElement.innerHTML;
        
        // Handle bullet points
        content = content.replace(/•\s/g, '<li>');
        content = content.replace(/<li>([^<]+)/g, '<li>$1</li>');
        
        // Wrap bullet points in a list
        if (content.includes('<li>')) {
            content = content.replace(/<li>/g, '<ul><li>');
            content = content.replace(/<\/li>[^<]*<ul>/g, '</li></ul><ul>');
            content = content.replace(/<\/li>(?![^<]*<ul|<\/ul>)/g, '</li></ul>');
        }
        
        // Handle paragraph breaks
        content = content.replace(/\n\n/g, '</p><p>');
        
        // Add paragraph tags if not already wrapped
        if (!content.startsWith('<p>') && !content.startsWith('<ul>')) {
            content = '<p>' + content;
        }
        if (!content.endsWith('</p>') && !content.endsWith('</ul>')) {
            content = content + '</p>';
        }
        
        answerElement.innerHTML = content;
    }
});