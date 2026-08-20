from esteiras_mcp.atlassian import plain_adf, plain_html

def test_plain_adf():
    value = {"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"INSS refin"}]}]}
    assert plain_adf(value) == "INSS refin"

def test_plain_html():
    assert plain_html("<p>Margem <b>nova</b></p>") == "Margem\nnova"
