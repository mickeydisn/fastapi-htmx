from fastapi_htmx.core.service.article import htmlArticleMain
from fastapi_htmx.core.service.article import htmlArticleH1
from fastapi_htmx.core.service.article import htmlArticleH2
from fastapi_htmx.core.service.article import htmlArticleH3
from fastapi_htmx.core.service.article import htmlArticleH4
from fastapi_htmx.core.service.content.makedown import htmlContentMDJson
from fastapi_htmx.core.service.content.makedown import htmlContentMD
from fastapi_htmx.core.service.content.makedown import htmlContentMDPyFunction

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlH1_Exemple3():
    content = """

<div class="formulair">
  <h2>Customize Theme</h2>

  <div id="controls">
    <!-- JS will inject input controls here -->
  </div>
</div>

<script>
  const variables = [
    'color-back', 'color-box', 'color-text'
  ];
  const properties = ['hue', 'sat', 'light', 'contrast'];

  const controlsDiv = document.getElementById('controls');

  variables.forEach(group => {
    const groupTitle = document.createElement('h3');
    groupTitle.textContent = group.replace('color-', '').toUpperCase();
    controlsDiv.appendChild(groupTitle);

    properties.forEach(prop => {
      const varName = `--${group}--${prop}`;
      const wrapper = document.createElement('p');
      wrapper.className = 'form-group';

      const label = document.createElement('label');
      label.for = varName;
      label.textContent = `${group} ${prop}`;

      const input = document.createElement('input');
      input.type = 'range';
      input.id = varName;
      input.min = prop === 'hue' ? 0 : 0;
      input.max = prop === 'hue' ? 360 : 100;
      input.value = getComputedStyle(document.documentElement).getPropertyValue(varName).trim().replace('%','');
      input.addEventListener('input', () => {
        document.documentElement.style.setProperty(varName, input.value + (prop === 'hue' ? '' : '%'));
      });

      wrapper.appendChild(label);
      wrapper.appendChild(input);
      controlsDiv.appendChild(wrapper);
    });
  });
</script>

    """

    return htmlArticleMain(
        "Exemple 2 : Article content components", content, isOpen=True
    )
