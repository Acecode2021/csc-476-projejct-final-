from pathlib import Path
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Rectangle
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

BASE=Path(__file__).resolve().parent
F=BASE/'figures';F.mkdir(exist_ok=True)
NAVY='#213d59'; BLUE='#eaf0f6'
def panel(ax,x,y,w,h,text,fs=11):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02',facecolor=BLUE,edgecolor=NAVY,lw=1.4))
 ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,color=NAVY)
def arrow(ax,a,b,label='',offset=(0,0)):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='<->',mutation_scale=12,color=NAVY,lw=1.3))
 ax.text((a[0]+b[0])/2+offset[0],(a[1]+b[1])/2+offset[1],label,ha='center',va='center',fontsize=9,color=NAVY,bbox=dict(facecolor='white',edgecolor='none',pad=2)) if label else None
def canvas(w=9,h=7):
 fig,ax=plt.subplots(figsize=(w,h));ax.set_xlim(0,10);ax.set_ylim(0,10);ax.axis('off');return fig,ax
def save(fig,name):
 fig.savefig(F/name,dpi=180,bbox_inches='tight',facecolor='white');plt.close(fig)
fig,ax=canvas()
panel(ax,1,7.6,8,1.6,'PRESENTATION\nBrowser • server-rendered HTML and CSS')
panel(ax,1,4.2,8,1.9,'APPLICATION\nFlask routes • session authentication • business rules\nJinja2 templates • SQLAlchemy models')
panel(ax,1,.9,8,1.6,'DATA\nSQLite • six relational tables')
arrow(ax,(5,7.6),(5,6.1),'HTTP requests / responses',(2.1,0))
arrow(ax,(5,4.2),(5,2.5),'Database operations',(1.8,0))
save(fig,'verified_architecture.png')
fig,ax=canvas(9,8)
ax.add_patch(Rectangle((3,.5),6.6,9,fill=False,edgecolor=NAVY,lw=1.5))
ax.text(6.3,9.7,'Maintenance portal: intended responsibilities',ha='center',fontsize=12,color=NAVY)
roles=[('Staff',8.3,['Submit ticket','Track own ticket']),('Technician',6.1,['Update assigned work','Submit field report']),('Supervisor',3.9,['Assign tickets','Create projects / tasks']),('Administrator',1.7,['Create user accounts','Assign role labels'])]
for role,y,uses in roles:
 panel(ax,.1,y-.4,2,.8,role,11)
 for dy,txt in zip([.45,-.45],uses):
  ax.add_patch(Ellipse((6.2,y+dy),4.7,.7,facecolor=BLUE,edgecolor=NAVY))
  ax.text(6.2,y+dy,txt,ha='center',va='center',fontsize=10)
  ax.plot([2.1,3.85],[y,y+dy],color=NAVY,lw=1)
ax.text(5,.1,'All roles authenticate. Diagram does not imply complete permission enforcement.',ha='center',fontsize=8,color=NAVY)
save(fig,'verified_usecases.png')
# Relational model as non-crossing association rows rather than misleading cardinality drawing.
fig,ax=canvas(9,8)
ax.text(5,9.6,'Parent entity → related records',ha='center',fontsize=14,color=NAVY)
rels=[('User','Ticket','reporter_id / technician_id'),('Ticket','TicketUpdate','ticket_id'),('User','TicketUpdate','author_id'),('User','Project','created_by'),('Project','Task','project_id'),('User','Task','assignee_id'),('User','FieldReport','technician_id'),('Ticket','FieldReport','ticket_id (optional)')]
for i,(l,r,k) in enumerate(rels):
 y=8.5-i*1.02
 panel(ax,.3,y-.28,2.1,.56,l,10);panel(ax,7.3,y-.28,2.3,.56,r,10)
 ax.add_patch(FancyArrowPatch((2.4,y),(7.3,y),arrowstyle='->',mutation_scale=11,color=NAVY))
 ax.text(4.9,y+.16,k,ha='center',fontsize=9,color=NAVY)
 ax.text(2.7,y-.25,'1',fontsize=9);ax.text(6.8,y-.25,'many',fontsize=8)
ax.text(5,.3,'Logical associations; nullability and constraint enforcement follow the implemented schema.',ha='center',fontsize=8,color=NAVY)
save(fig,'verified_relationships.png')

TEAM=[('Ogundele, Tobiloba James','E054654'),('Aderinto, Kunle Abraham','E055233'),('Olusola, Ayomide Emmanuel','E055067'),('Alonge, Ayobami Blessing','E054861')]
TITLE='AUTOMATION OF HELP DESK, PROJECT TRACKING AND FIELD REPORTING FOR THE MAINTENANCE DEPARTMENT, UNIVERSITY OF IBADAN'
doc=Document()
for sec in doc.sections:
 sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.top_margin=Cm(2.4);sec.bottom_margin=Cm(2.4);sec.left_margin=Cm(3);sec.right_margin=Cm(2.5)
styles=doc.styles
for name in ['Normal','Body Text']:
 styles[name].font.name='Times New Roman';styles[name].font.size=Pt(12)
 styles[name].paragraph_format.line_spacing=1.5
 styles[name].paragraph_format.space_after=Pt(6)
 styles[name].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY
for name,size in [('Title',17),('Heading 1',15),('Heading 2',13),('Heading 3',12)]:
 styles[name].font.name='Times New Roman';styles[name].font.size=Pt(size);styles[name].font.bold=True;styles[name].font.color.rgb=RGBColor.from_string('213D59')
 styles[name].paragraph_format.space_before=Pt(12);styles[name].paragraph_format.space_after=Pt(8)
 styles[name].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.LEFT
styles['Caption'].font.name='Times New Roman';styles['Caption'].font.size=Pt(10);styles['Caption'].font.color.rgb=RGBColor.from_string('213D59')
styles['Caption'].paragraph_format.line_spacing=1.0

styles.add_style('Front Matter Heading', WD_STYLE_TYPE.PARAGRAPH).base_style=styles['Normal']
for custom in ['Figure Caption','Table Caption']:
 styles.add_style(custom, WD_STYLE_TYPE.PARAGRAPH).base_style=styles['Caption']

def field(p,code,placeholder='Update this field in Microsoft Word to display the index.'):
 r=p.add_run();beg=OxmlElement('w:fldChar');beg.set(qn('w:fldCharType'),'begin');r._r.append(beg)
 inst=OxmlElement('w:instrText');inst.set(qn('xml:space'),'preserve');inst.text=code;p.add_run()._r.append(inst)
 sep=OxmlElement('w:fldChar');sep.set(qn('w:fldCharType'),'separate');p.add_run()._r.append(sep)
 p.add_run(placeholder)
 end=OxmlElement('w:fldChar');end.set(qn('w:fldCharType'),'end');p.add_run()._r.append(end)
def pg(sec,fmt,start):
 el=OxmlElement('w:pgNumType');el.set(qn('w:fmt'),fmt);el.set(qn('w:start'),str(start));sec._sectPr.append(el)
 sec.footer.is_linked_to_previous=False
 p=sec.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 field(p,' PAGE ','')
 for r in p.runs:r.font.size=Pt(10)
def centered(text,size=12,bold=False):
 p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.line_spacing=1.2
 r=p.add_run(text);r.font.size=Pt(size);r.bold=bold
 if text in ['CERTIFICATION','DEDICATION','ACKNOWLEDGEMENT','REPORT PREPARATION NOTE','TEAM MEMBERS’ PARTICIPATION INPUT','TEAM LEADER’S CONFIRMATION','ABSTRACT','LIST OF FIGURES','LIST OF TABLES','LIST OF ABBREVIATIONS']:
  p.style='Front Matter Heading'
 return p
def body(text):
 return doc.add_paragraph(text)
def page_break():
 # Avoid blank sheets caused by adjacent explicit page breaks.
 children=list(doc.element.body)
 if children and children[-1].tag==qn('w:sectPr'): children=children[:-1]
 if children:
  e=children[-1]
  if e.tag==qn('w:p') and e.findall('.//'+qn('w:br')) and not ''.join(e.itertext()).strip():
   return
 doc.add_page_break()

def front(title):
 page_break();centered(title,14,True)
def heading(title,level=1):
 p=doc.add_heading(title,level);return p

def table_page(caption,headers,rows):
 page_break()
 p=doc.add_paragraph(caption,'Table Caption');p.paragraph_format.keep_with_next=True
 t=doc.add_table(rows=1,cols=len(headers));t.style='Table Grid'
 for c,txt in zip(t.rows[0].cells,headers):c.text=txt
 for row in rows:
  for c,txt in zip(t.add_row().cells,row):c.text=txt
 for i,row in enumerate(t.rows):
  trpr=row._tr.get_or_add_trPr();cant=OxmlElement('w:cantSplit');trpr.append(cant)
  if i==0:
   repeat=OxmlElement('w:tblHeader');trpr.append(repeat)
  for c in row.cells:
   if i==0:
    shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'EAF0F6');c._tc.get_or_add_tcPr().append(shade)
   for p in c.paragraphs:
    p.paragraph_format.line_spacing=1.05;p.paragraph_format.space_after=Pt(5);p.paragraph_format.space_before=Pt(4);p.alignment=WD_ALIGN_PARAGRAPH.LEFT
    for r in p.runs:r.font.size=Pt(10);r.bold=(i==0)
 page_break()

centered('UNIVERSITY OF IBADAN',14,True)
centered('DEPARTMENT OF COMPUTER SCIENCE\nFACULTY OF SCIENCE',12,True)
doc.add_paragraph()
centered(TITLE,16,True)
centered('BY',12,True)
for name,num in TEAM:centered(name+' — '+num,12,True)
doc.add_paragraph()
centered('SUBMITTED TO\nTHE DEPARTMENT OF COMPUTER SCIENCE,\nFACULTY OF SCIENCE,\nUNIVERSITY OF IBADAN, IBADAN, NIGERIA',11,True)
centered('IN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE AWARD OF THE DEGREE OF BACHELOR OF SCIENCE (B.Sc.) IN COMPUTER SCIENCE',11,True)
centered('CSC 476: [OFFICIAL COURSE TITLE]',11,True)
centered('SUPERVISED BY PROFESSOR OLADEJO',11,True)
centered('[MONTH AND YEAR OF SUBMISSION]',11,True)
sec=doc.add_section(WD_SECTION_START.NEW_PAGE);pg(sec,'lowerRoman',1)
centered('CERTIFICATION',14,True)
body('The project titled “'+TITLE.title()+'” is submitted as a group project by the following students of the Department of Computer Science, Faculty of Science, University of Ibadan:')
for name,num in TEAM:body(name+' ('+num+').')
body('The group project is supervised by Professor Oladejo, who is also the CSC 476 course lecturer.')
body('The supervisor and Head of Department should review the final work and confirm the required certification wording before signing. No approval or signature is implied by this draft.')
for label in ['Professor Oladejo (Supervisor)','[HEAD OF DEPARTMENT NAME AND TITLE]']:
 doc.add_paragraph();body('________________________________        __________________')
 body(label+'                                    Date')
front('DEDICATION')
body('We dedicate this project to our families and loved ones for their encouragement, patience and support throughout our academic journey.')
body('We also dedicate this work to all students who value teamwork, shared responsibility and the pursuit of knowledge.')
front('ACKNOWLEDGEMENT')
body('We thank Professor Oladejo, our project supervisor and CSC 476 course lecturer, for supervising this group project.')
body('We submit this report jointly as Ogundele, Tobiloba James (E054654), Aderinto, Kunle Abraham (E055233), Olusola, Ayomide Emmanuel (E055067), and Alonge, Ayobami Blessing (E054861). The participation statement records our individual responsibilities and remains subject to the team leader’s verification.')

front('REPORT PREPARATION NOTE')
body('Document status: consolidated academic report draft for review. The report describes a working prototype, not a university-deployed service. The title expands UI as University of Ibadan. The group must confirm the title with the lecturer.')
body('Professor Oladejo is the confirmed project supervisor and course lecturer. The HOD, official CSC 476 course title and submission date remain labelled placeholders. The deadline has not been specified. Ogundele, Tobiloba James (E054654) is the team leader, as confirmed by the group representative.')
body('No interviews, site observations or participant usability studies have been conducted. All displayed application records are synthetic. Executed test results are distinguished from unexecuted checks. Known defects are retained explicitly.')
body('Working format: A4, Times New Roman 12 pt and 1.5 line spacing. These settings are editorial choices because the supplied template did not specify them. Figures and tables are isolated on separate pages. Confirm all lecturer-specific requirements before submission.')
body('The contents, figure and table lists are populated in the supplied files. Page numbers refer to the supplied layout. After editing in Word, update all fields with Ctrl+A then F9 and check pagination before printing. The accompanying PDF preserves the checked page layout.')
front('TEAM MEMBERS’ PARTICIPATION INPUT')
body('Team leader: Ogundele, Tobiloba James (E054654). The proposed division of responsibilities is presented below for the team leader’s review. Completed contributions and supporting evidence must be confirmed before this section is submitted.')
body('The table is placed on the following page to comply with the departmental separate-table-page instruction. Confirm the preferred front-matter position with the lecturer.')
table_page('Team members’ participation input — proposed allocation for leader verification',
 ['Member / matriculation number','Proposed responsibility','Completed work / evidence to verify'],[
 ['Ogundele, Tobiloba James\nE054654','Team coordination and report compilation. Coordinate tasks, monitor progress and bring the report sections together.','Completion awaiting confirmation. The leader should identify coordination and compilation work actually completed, supported by task records or report revisions where available.'],
 ['Aderinto, Kunle Abraham\nE055233','Literature review and requirements documentation. Review relevant sources and organise the system requirements.','Completion awaiting confirmation. Record the literature summaries, reference entries and requirements sections personally prepared or reviewed.'],
 ['Olusola, Ayomide Emmanuel\nE055067','System design and implementation review. Review database relationships, application modules and proposed improvements.','Completion awaiting confirmation. Identify diagrams, design notes or code changes personally produced or reviewed; include evidence only where it exists.'],
 ['Alonge, Ayobami Blessing\nE054861','Testing, interface review and user documentation. Check workflows, record issues and review the installation and user guides.','Completion awaiting confirmation. Record tests personally performed, issues documented and guide sections prepared or reviewed.']])
centered('TEAM LEADER’S CONFIRMATION',13,True)
body('The team leader must verify that the participation entries accurately describe every member’s actual contribution before approving and submitting this section on behalf of the group.')
body('Ogundele, Tobiloba James — E054654')
body('Signature: ____________________      Date: ____________________')
front('ABSTRACT')
body('Maintenance information management requires a connection between reported faults, assigned work and documented outcomes. This project develops a web-based prototype for help desk management, project tracking and field reporting intended for the Maintenance Department, University of Ibadan. It addresses the need to demonstrate these related functions in a common application. The initial requirements are literature-informed; the university’s existing procedures have not been investigated through interviews or direct observation.')
body('An iterative development approach was used to translate provisional requirements into a modular application and relational database. Python and Flask provide request processing, SQLite stores records, and Jinja2, HTML and CSS provide server-rendered interfaces. The implementation includes users, tickets, ticket updates, projects, tasks and field reports. Evaluation used an isolated test database and synthetic demonstration records, with browser navigation and screenshot capture through Playwright and Chromium.')
body('The prototype supports core ticket operations, task assignment and progress updates, structured field reports and summary views. The verification test run completed with 17 passing tests, and eight genuine application screenshots were captured. These results demonstrate selected functions under test conditions, not institutional effectiveness. Record-level authorisation, validation, administrative functions and workflow controls remain incomplete. Stakeholder validation, security improvements and broader evaluation are recommended before any operational deployment.')
front('TABLE OF CONTENTS');field(doc.add_paragraph(),' TOC \\o "1-3" \\t "Front Matter Heading,1" \\h \\z \\u ')
front('LIST OF FIGURES');field(doc.add_paragraph(),' TOC \\t "Figure Caption,1" \\h ')
content=(BASE/'Professional_Report_Content.md').read_text()
front('LIST OF TABLES');field(doc.add_paragraph(),' TOC \\t "Table Caption,1" \\h ')
body('Front matter: Team members’ participation input (unnumbered).')
front('LIST OF ABBREVIATIONS')
for term,meaning in [('CMMS','Computerised Maintenance Management System'),('CSS','Cascading Style Sheets'),('CSRF','Cross-Site Request Forgery'),('HTML','Hypertext Markup Language'),('HTTP','Hypertext Transfer Protocol'),('ICT','Information and Communication Technology'),('ORM','Object-Relational Mapping'),('UI','University of Ibadan, in the project title'),('UML','Unified Modeling Language'),('URL','Uniform Resource Locator')]:body(term+' — '+meaning)
sec=doc.add_section(WD_SECTION_START.NEW_PAGE);pg(sec,'decimal',1)
sec.header.is_linked_to_previous=False
p=sec.header.paragraphs[0];p.text='CSC 476  |  MAINTENANCE INFORMATION SYSTEM  |  REVIEW DRAFT';p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
for r in p.runs:r.font.name='Arial';r.font.size=Pt(8);r.font.color.rgb=RGBColor.from_string('64748B')
lines=content.splitlines();i=0;first=True
while i<len(lines):
 s=lines[i].strip();i+=1
 if not s:continue
 if s.startswith('# '):
  if not first:page_break()
  heading(s[2:],1);first=False
 elif s.startswith('## '):heading(s[3:],2)
 elif s.startswith('### '):heading(s[4:],3)
 elif s.startswith('TABLE: '):
  title=s[7:];headers=[v.strip() for v in lines[i].split('|')];i+=1;rows=[]
  while lines[i].strip()!='ENDTABLE':rows.append([v.strip() for v in lines[i].split('|')]);i+=1
  i+=1;table_page(title,headers,rows)
 elif s.startswith('FIGURE: '):
  path,caption=s[8:].split(' | ',1);page_break()
  with Image.open(BASE/path) as im:w,h=im.size
  width=min(6.05,7.9*w/h)
  p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.line_spacing=1;p.paragraph_format.keep_with_next=True
  p.add_run().add_picture(str(BASE/path),width=Inches(width))
  p=doc.add_paragraph(caption,'Figure Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  p=doc.add_paragraph('Source: project application (synthetic data), captured with Chromium.' if 'fig4_' in path else 'Source: project design, derived from the prototype.');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  for r in p.runs:r.font.size=Pt(9);r.italic=True
  page_break()
 elif re.match(r'^\d+\. ',s):
  p=doc.add_paragraph(s,style='Normal');p.paragraph_format.left_indent=Cm(.4)
 else:body(s)
# Enable Word field refresh.
setting=OxmlElement('w:updateFields');setting.set(qn('w:val'),'true');doc.settings.element.append(setting)
doc.core_properties.title=TITLE.title();doc.core_properties.subject='CSC 476 group project: consolidated prototype report'
doc.core_properties.author='; '.join(n+' ('+m+')' for n,m in TEAM)
doc.core_properties.comments='Supervisor and course lecturer: Professor Oladejo. Team leader: Ogundele, Tobiloba James (E054654).'
doc.core_properties.keywords='University of Ibadan; CSC 476; maintenance; prototype; review draft'
output=BASE/'CSC476_Final_Project_Report.docx';doc.save(output)
doc.save(BASE/'CSC476_Group_Project_Report_Professional.docx')
print(output)
print('Paragraphs:',len(doc.paragraphs),'Tables:',len(doc.tables),'Images:',len(doc.inline_shapes))
