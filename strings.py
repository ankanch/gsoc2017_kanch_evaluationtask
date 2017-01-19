TABLE_HEAD = """<table class="table table-striped table-hover ">
  <thead>
  <tr>
    <th>Domain</th>
    <th>Peptide</th>
    <th>Start</th>
    <th>Stop</th>
    <th>Sequence</th>
    <th>Peptide Score</th>
    <th>Peptide Count</th>
    <th>Protein Score</th>
    <th>Protein Count</th>
    <th>Score</th>
  </tr>
  </thead>
  <tbody>"""
					 				
TABLE_C_START =   """<tr>
    <td>"""
TABLE_C_REP = """</td>
    <td>"""
TABLE_C_END = """</td>
  </tr>"""
TABLE_TAIL = """  </tbody>
</table>"""

#for buttons of result page
BUTTON_HEAD = """<a href="javascript:showResult('div_"""
BUTTON_A = """')" class="btn btn-raised btn-info" id="button_"""
BUTTON_B = """">"""
BUTTON_TAIL = """</a>"""

#for divs of result page
DIV_HEAD = """<div id=\"div_"""
DIV_A = """\">"""
DIV_TAIL= """</div>"""