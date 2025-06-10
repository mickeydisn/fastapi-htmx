from fastapi_htmx.core.service.article import htmlArticleH2
from fastapi_htmx.core.service.article import htmlArticleMain
from fastapi_htmx.core.service.content.makedown import htmlContentMD
from fastapi_htmx.core.service.content.makedown import htmlContentMDPyFunction

from fastapi_htmx.core.service.content.makedown import htmlContentMD_exemple
from fastapi_htmx.core.service.content.chart import htmlContentChart_exemple
from fastapi_htmx.core.service.content.panda_chart import htmlContentPandaChartTimeSerie_exemple


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlHtmxExmple_component_md():
    return htmlArticleMain('Componenet MD', "".join([
            # htmlContentMDPyFunction(htmlContentMD_exemple),
            htmlContentMD_exemple()
        ]),
        isOpen=True
    )


def htmlHtmxExmple_component_chat():
    return htmlArticleMain('Componenet Chart', "".join([
            htmlContentMDPyFunction(htmlContentChart_exemple),
            htmlContentChart_exemple()
        ]),
        isOpen=True
    )


def htmlHtmxExmple_component_panda_chat():
    return htmlArticleMain('Componenet PandaChart', "".join([
            htmlContentMDPyFunction(htmlContentPandaChartTimeSerie_exemple),
            htmlContentPandaChartTimeSerie_exemple()
        ]),
        isOpen=True
    )

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
