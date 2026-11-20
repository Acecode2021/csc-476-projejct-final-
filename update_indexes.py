import uno
from pathlib import Path
from com.sun.star.beans import PropertyValue

def prop(k,v):
 p=PropertyValue();p.Name=k;p.Value=v;return p
ctx=uno.getComponentContext()
resolver=ctx.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',ctx)
remote=resolver.resolve('uno:socket,host=127.0.0.1,port=2002;urp;StarOffice.ComponentContext')
desktop=remote.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop',remote)
b=Path('/home/user/CSC476_Semester_Project/02_Final_Writeup')
doc=desktop.loadComponentFromURL(uno.systemPathToFileUrl(str(b/'CSC476_Final_Project_Report.docx')),'_blank',0,(prop('Hidden',True),))
indexes=doc.getDocumentIndexes();print('Indexes',indexes.getCount())
# Ensure dotted tab leaders on generated entry styles.
styles=doc.StyleFamilies.getByName('ParagraphStyles')
for name in styles.getElementNames():
 if name.startswith(('Contents ','Illustration Index','Table Index')):
  style=styles.getByName(name)
  try:
   tab=uno.createUnoStruct('com.sun.star.style.TabStop');tab.Position=15400;tab.Alignment=uno.Enum('com.sun.star.style.TabAlign','RIGHT');tab.FillChar='.'
   style.ParaTabStops=(tab,);style.ParaAdjust=0;style.CharHeight=10;style.ParaBottomMargin=70
  except Exception as exc:print(name,exc)
for _ in range(3):
 for i in range(indexes.getCount()):
  index=indexes.getByIndex(i);index.update()
 doc.refresh()
print('Pages',doc.CurrentController.PageCount)
out=b/'CSC476_Final_Project_Report_60plus.docx'
doc.storeAsURL(uno.systemPathToFileUrl(str(out)),(prop('FilterName','Office Open XML Text'),prop('Overwrite',True)))
doc.storeToURL(uno.systemPathToFileUrl(str(b/'CSC476_Final_Project_Report_60plus.pdf')),(prop('FilterName','writer_pdf_Export'),prop('Overwrite',True)))
doc.close(True)
print('Saved DOCX and PDF')
