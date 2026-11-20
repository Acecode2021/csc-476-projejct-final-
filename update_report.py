from pathlib import Path
import zipfile
b=Path('/home/user/CSC476_Semester_Project/02_Final_Writeup')
p=b/'_parts/part4_ch4.md'
s=p.read_text()
a=s.index('The system was developed using'); z=s.index('\n\n',a)
s=s[:a]+'The prototype was developed in a Linux workspace using Python 3.13, Flask and SQLite. Chromium, controlled through Playwright, was used to capture the application screens. No Firefox, Edge or participant-based usability evaluation has been verified.'+s[z:]
s=s.replace('Figures 4.1 to 4.8 show the main screens of the implemented system, captured from the running application.','Figures 4.1 to 4.8 are genuine browser screenshots of the running prototype. All names, tickets, projects and field reports displayed are synthetic demonstration records, not records collected from the University of Ibadan. Source: project application, captured using Playwright and Chromium.')
s=s.replace('with Visual Studio Code as the editor','using workspace file-editing tools')
s=s.replace('4. **Usability checks:** the main user tasks (logging a fault, checking its status, filing a field report) were exercised end-to-end in a real browser during development, and the interface was reviewed for clarity, consistency and feedback.','4. **Browser inspection:** login and navigation to eight screens were exercised in Chromium for screenshot capture. Participant usability testing has not been conducted.')
s=s.replace('| Usability checks (browser walkthrough of the main tasks) | Informal | Completed | 0 |','| Participant usability testing | Not conducted | — | — |')
s=s.replace('Counts match the database records | Pass — counts matched database records','Dashboard renders expected headings | Pass — expected headings were present')
s=s.replace('Generate ticket report with date filter','Generate ticket report with status filter')
p.write_text(s)
parts=sorted((b/'_parts').glob('part*.md'))
text='\n'.join(p.read_text() for p in parts)
notice='> **WORKING DRAFT — NOT READY FOR SUBMISSION.** Chapter Four contains actual prototype screenshots using synthetic demonstration data. Earlier statements about institutional observations, interviews, staff feedback and completed field research are unverified and must not be submitted as factual findings. References, diagrams, permissions, formatting and remaining implementation claims still require review. UI in the project title should be confirmed as University of Ibadan, not assumed to mean user interface.\n\n'
text=notice+text
text=text.replace('self.resolved_at = datetime.utcnow\n','self.resolved_at = datetime.utcnow()\n')
(b/'CSC476_Final_Project_Report.md').write_text(text)
with zipfile.ZipFile(b/'Application_Screenshots.zip','w',zipfile.ZIP_DEFLATED) as f:
 for img in sorted((b/'figures').glob('fig4_*.png')): f.write(img,img.name)
 f.writestr('README.txt','Eight genuine screenshots of the Flask prototype captured with Chromium. All displayed records are synthetic demonstration data, not university operational records. These screenshots do not constitute participant usability testing.\n')
