import inspect

from app.core.service.article import htmlArticleH2
from app.core.service.article import htmlArticleMain
from app.core.service.content.makedown import htmlContentMD
from app.core.service.content.makedown import htmlContentMDPyFunction

from app.core.service.content.makedown import htmlContentMD_exemple
from app.core.service.content.chart import htmlContentChart_exemple
from app.core.service.content.panda_chart import htmlContentPandaChartTimeSerie_exemple


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

