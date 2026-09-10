from esteiras_mcp.atlassian import plain_adf, plain_html

def test_plain_adf():
    value = {"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"INSS refin"}]}]}
    assert plain_adf(value) == "INSS refin"
    assert plain_adf({"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"INSS refin"},{"type":"hardBreak"},{"type":"text","text":"teste"}]}]}) == "INSS refin\nteste"
    

def test_plain_html():
    assert plain_html("<p>Margem <b>nova</b></p>") == "Margem\nnova"
    assert plain_html("<p>Margem <b>nova</b><br>teste</p>") == "Margem\nnova\nteste"
    assert plain_html("<p>Margem <b>nova</b><br>teste<br>refin</p>") == "Margem\nnova\nteste\nrefin"