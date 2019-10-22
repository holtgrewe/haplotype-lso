"""Setup of Dash UI."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from logzero import logger

from . import settings
from .settings import (
    MIN_IDENTITY_GREEN,
    MIN_IDENTITY_YELLOW,
    FONT_COLOR_GREEN,
    FONT_COLOR_YELLOW,
    FONT_COLOR_RED,
    BG_COLOR_GREEN,
    BG_COLOR_YELLOW,
    BG_COLOR_RED,
)
from ..haplotyping import HAPLOTYPE_NAMES
from .. import __version__


def render_navbar():
    """Render the site navbar"""
    return dbc.Navbar(
        dbc.Container(
            children=[
                # Use row and col to control vertical alignment of logo / brand
                dbc.NavbarBrand(
                    children=[html.I(className="fas fa-carrot mr-1"), settings.HOME_BRAND],
                    id="page-brand",
                ),
                dbc.Nav(
                    dbc.NavItem(
                        dbc.NavLink(
                            dcc.Upload(
                                id="upload-data",
                                children=[
                                    html.I(className="fas fa-cloud-upload-alt mr-1"),
                                    "upload files",
                                ],
                                multiple=True,
                            ),
                            className="btn btn-outline-secondary",
                            active=True,
                        )
                    )
                ),
            ]
        ),
        color="primary",
        dark=True,
        id="page-navbar",
    )


def render_page_content_empty_children():
    """Return page content when there's no content (no sequence has been uploaded yet)."""
    return [
        html.Div(
            children=[
                html.Div(
                    children=[
                        "Click ",
                        html.Span(
                            children=[
                                html.I(className="fas fa-cloud-upload-alt mr-1"),
                                "upload files",
                            ],
                            className="badge badge-secondary ml-1 mr-1",
                        ),
                        'upload files on the top right to upload one or more .fasta, .fastq, "'
                        ".scf, or .ab1 files.  You can find a ZIP file with some examples ",
                        html.A(
                            children=[html.I(className="fas fa-download mr-1"), "here"],
                            href="/dash/assets/clsify_example.zip",
                            className="badge badge-primary",
                        ),
                        ".",
                    ]
                )
            ]
        ),
        html.Div(children=[dash_table.DataTable(id="blast-table")], style={"display": "none"}),
        html.Div(
            children=[dash_table.DataTable(id="haplotyping-table")], style={"display": "none"}
        ),
        html.Div(children=["placeholder"], id="blast-current-match", style={"display": "none"}),
    ]


def render_page_content_empty():
    return html.Div(
        children=[
            html.Div(render_page_content_empty_children(), className="text-center text-muted")
        ],
        id="page-content",
    )


def render_main_content():
    """Render page main content"""
    return html.Div(
        children=[dbc.Row(dbc.Col(children=[render_page_content_empty()]))],
        className="container pt-3",
    )


def render_footer():
    """Render page footer"""
    return html.Footer(
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Span("clsify v%s" % __version__, className="text-muted")
                            ],
                            className="col-6",
                        ),
                        html.Div(
                            children=[
                                html.A(
                                    children=[
                                        html.I(className="fab fa-github mr-1"),
                                        "GitHub Project",
                                    ],
                                    href="https://github.com/holtgrewe/clsify",
                                    className="text-muted",
                                )
                            ],
                            className="col-6 text-right",
                        ),
                    ],
                    className="row",
                )
            ],
            className="container",
        ),
        className="footer",
    )


def render_tab_summary(session_data):
    logger.info("Rendering Summary Tab")
    col_ids = list(session_data["blast"].columns)
    columns = [{"name": col, "id": col} for col in col_ids]
    style_cell = {"font-family": "sans-serif"}
    style_cell_conditional = [
        {"if": {"column_id": "query"}, "textAlign": "left"},
        {"if": {"column_id": "subject"}, "textAlign": "left"},
    ]
    style_data_conditional = [
        {
            "if": {
                "column_id": "identity",
                "filter_query": "{identity} < %f" % MIN_IDENTITY_YELLOW,
            },
            "color": FONT_COLOR_RED,
            "backgroundColor": BG_COLOR_RED,
        },
        {
            "if": {
                "column_id": "identity",
                "filter_query": "{identity} >= %f" % MIN_IDENTITY_YELLOW,
            },
            "color": FONT_COLOR_YELLOW,
            "backgroundColor": BG_COLOR_YELLOW,
        },
        {
            "if": {
                "column_id": "identity",
                "filter_query": "{identity} >= %f" % MIN_IDENTITY_GREEN,
            },
            "color": FONT_COLOR_GREEN,
            "backgroundColor": BG_COLOR_GREEN,
        },
    ]
    style_header = {"text-align": "center", "fontWeight": "bold"}
    df = session_data["summary"]
    df.loc[:, "identity"] = df.loc[:, "identity"].map(
        lambda x: str(round(float(x), 1)) if x != "-" else x
    )
    table = dash_table.DataTable(
        id="summary-table",
        columns=[{"name": i, "id": i} for i in df.columns if i != "alignment"],
        data=[
            {k: v for k, v in record.items() if k != "alignment"}
            for record in df.to_dict("records")
        ],
        style_cell=style_cell,
        style_cell_conditional=style_cell_conditional,
        style_data_conditional=style_data_conditional,
        style_header=style_header,
    )
    return [dcc.Loading(table)]


def render_tab_blast(session_data):
    logger.info("Rendering BLAST Tab")
    col_ids = list(session_data["blast"].columns)
    columns = [{"name": col, "id": col} for col in col_ids]
    style_cell = {"font-family": "sans-serif"}
    style_cell_conditional = [
        {"if": {"column_id": "query"}, "textAlign": "left"},
        {"if": {"column_id": "subject"}, "textAlign": "left"},
    ]
    style_data_conditional = [
        {
            "if": {
                "column_id": "identity",
                "filter_query": "{identity} < %f" % MIN_IDENTITY_YELLOW,
            },
            "color": FONT_COLOR_RED,
            "backgroundColor": BG_COLOR_RED,
        },
        {
            "if": {
                "column_id": "identity",
                "filter_query": "{identity} >= %f" % MIN_IDENTITY_YELLOW,
            },
            "color": FONT_COLOR_YELLOW,
            "backgroundColor": BG_COLOR_YELLOW,
        },
        {
            "if": {
                "column_id": "identity",
                "filter_query": "{identity} >= %f" % MIN_IDENTITY_GREEN,
            },
            "color": FONT_COLOR_GREEN,
            "backgroundColor": BG_COLOR_GREEN,
        },
    ]
    style_header = {"text-align": "center", "fontWeight": "bold"}
    df = session_data["blast"]
    df.loc[:, "identity"] = df.loc[:, "identity"].map(lambda x: str(round(float(x), 1)))
    table = dash_table.DataTable(
        id="blast-table",
        columns=[{"name": i, "id": i} for i in df.columns if i != "alignment"],
        data=[
            {k: v for k, v in record.items() if k != "alignment"}
            for record in df.to_dict("records")
        ],
        style_cell=style_cell,
        style_cell_conditional=style_cell_conditional,
        style_data_conditional=style_data_conditional,
        style_header=style_header,
        row_selectable="single",
    )
    blast_match_div = html.Div(children=["42"], id="blast-current-match")
    return [dcc.Loading(table), dcc.Loading(blast_match_div)]


def _pos_neg(x):
    return x.replace("_neg", "-").replace("_pos", "+")


def render_tab_haplotyping(session_data):
    logger.info("Rendering Haplotying Tab")
    df = session_data["haplotyping"]
    columns = [{"name": col, "id": col} for col in df.columns]
    style_cell = {"font-family": "sans-serif"}
    style_header = {"text-align": "center", "fontWeight": "bold"}
    table = dash_table.DataTable(
        id="haplotyping-table",
        columns=[{"name": _pos_neg(i), "id": _pos_neg(i)} for i in df.columns],
        data=[
            {_pos_neg(key): value for key, value in record.items()}
            for record in df.to_dict("records")
        ],
        style_cell=style_cell,
        style_header=style_header,
    )
    # blast_match = html.Div(id="blast-haplotyping-children", children=[])
    # blast_match_div = html.Div(children=["0815"], id="haplotyping-current-match")
    return [dcc.Loading(table)]  # , dcc.Loading(blast_match_div)]


def render_hidden():
    return html.Div(children=[html.Div(id="hidden-data", style={"display": "none"})])


def build_layout():
    """Build the overall Dash app layout"""
    return html.Div(
        children=[
            # Represents the URL bar, doesn't render anything.
            dcc.Location(id="url", refresh=False),
            # Navbar, content, footer.
            render_navbar(),
            render_main_content(),
            render_footer(),
            render_hidden(),
        ],
        id="_dash-app-content",  # make pytest-dash happy
    )
