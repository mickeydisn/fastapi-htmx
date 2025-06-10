import os
import uuid

import json
import pandas as pd
import itertools


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlMenuLabelItem_ClickOnLabel(name, url):
    return f"""
    <label
        class="hover-active"
        hx-trigger="click" 
        hx-get="{url}" 
        hx-target="#nav-content"
        hx-swap="afterbegin"
    ><h4>
        <div>{name}</div>
        <div  style="display:flex;">
        </div>
    </h4></label>
    """


def htmlMenuLabelItem_ClickOnIcon(name, url, icon="🚀"):
    return f"""
    <label><h4>
        <div>{name}</div>
        <div  style="display:flex;">
            <span class="icone hover-active"
                hx-trigger="click" 
                hx-get="{url}" 
                hx-target="#nav-content"
                hx-swap="afterbegin scroll:#nav-center:top"
            >
                {icon}
            </span>
        </div>
    </h4></label>
    """
