
document.addEventListener("DOMContentLoaded", convertAfterSwap);
document.body.addEventListener("htmx:afterSettle", convertAfterSwap);

function convertAfterSwap() {
    console.log("Hello");
    convertAfterSwapMD();
    convertAfterSwapRemove();
}
function convertAfterSwapRemove() {
    {
        // Catch Clone element - ie: element with the same ID - and remove all thier are't in class removeClone.
        // then remove the class removeClone
        const elements = document.querySelectorAll('.removeClone');
        console.log('Remove:', elements)

        elements.forEach(el => {
            const id = el.id;
            if (!id) return; // skip elements without IDs
            console.log('Remove Id:', id)

            // Find all elements with the same ID
            const allWithId = document.querySelectorAll(`#${id}`);
            allWithId.forEach(item => {
                // Remove clones (same ID, but not the main .removeClone one)
                if (! item.classList.contains("removeClone")) {
                    console.log('Remove - Item')
                    item.remove();
                }
            });
        })
    }
    {
        // Remove the marker class from the main element
        const elements = document.querySelectorAll('.removeClone');
        elements.forEach(el => {
            const id = el.id;
            if (!id) return; // skip elements without IDs
            console.log('Remove - Class')
            el.classList.remove('removeClone');
        })
    }
}

function convertAfterSwapMD() {

    // init the markdown parser
    marked.setOptions({
        breaks: true,
        headerIds: false,
        mangle: false,
        langPrefix: 'language-',
        highlight: function(code, lang) {
            return hljs.highlightAuto(code).value;
        }
    });

    // Catch new Markdown element
    const elements = document.querySelectorAll('.markdown');
    elements.forEach(el => {

        // Clean up: remove trailing spaces and duplicate blank lines
        let raw = el.textContent
            .split('\n')
            .map(line => line.replace(/\s+$/, ''))   // Trim trailing spaces
            .join('\n')
            .replace(/\n{3,}/g, '\n\n');             // Reduce multiple blank lines to one

        // Parse and render Markdown
        el.innerHTML = marked.parse(raw.trim());

        // Highlight code blocks
        el.querySelectorAll('pre code').forEach(block => {
            hljs.highlightElement(block);
        });

        // Update class to tag it as already processed
        el.classList.remove('markdown');
        el.classList.add('markdown-loaded');
    });

    
    /*
    // Catch new script element
    const elementsScript = document.querySelectorAll('.run-script');
    console.log(elementsScript)
    elements.forEach(el => {

        const scripts = el.querySelectorAll("script");
        scripts.forEach(script => {
            const newScript = document.createElement("script");
            if (script.src) {
                newScript.src = script.src;
            } else {
                newScript.textContent = script.textContent;
            }
            document.body.appendChild(newScript);
            // Clean up (optional)
            document.body.removeChild(newScript);
        });

        // Update class to tag it as already processed
        el.classList.remove('run-script');
    });
    */
}
