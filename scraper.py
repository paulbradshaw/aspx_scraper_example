# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library
# This example shows how to follow the links to each page
import scraperwiki
import mechanize
import re

url = 'http://slmpd.org/CrimeReport.aspx'
#create an empty dictionary to store data
record = {}

br = mechanize.Browser()
# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)
html = response.read()
#PDF links look like: javascript:__doPostBack('GridView1$ctl15$lnkdownloadS','') - note the S (the number 15 changes)
#CSV links look like: javascript:__doPostBack('GridView1$ctl15$lnkdownloadD','') - note the D
#this comes after <a id="GridView1_lnkdownloadS_14" HeaderText="Sum" 
pdfs = re.findall("doPostBack('GridView1$ctl[0-9]*$lnkdownloadS')", html)
csvs = re.findall("doPostBack('GridView1$ctl[0-9]*$lnkdownloadD')", html)
for pdf in pdfs:
    print 'PDF:', pdf

#new function to find forms with id="form1"
def is_sblock_form(form):
    #form.set_all_readonly(False) # allow changing the .value of all controls
    return "id" in form.attrs and form.attrs['id'] == "form1"

#page links look like: javascript:__doPostBack('GridView1','Page$5')
#and use style="color:White;"
pages = re.findall('style="color:White;">[0-9]*</a>', html)
pagenum = len(pages)+1
print "There are", pagenum, "pages"
for page in pages:
    pageasstr = str(page.replace('style="color:White;">','').replace('</a>',''))
    print "Pages found on p1:", pageasstr
    #The doPostBack is repeated with the page number inserted
    #javascript:__doPostBack('GridView1','Page$4')
    #form does not have a name, so:
    #https://stackoverflow.com/questions/10495313/mechanize-select-form-using-id
    #br.select_form(name='form1')
    br.select_form(predicate=is_sblock_form)
    br.form.set_all_readonly(False)
    #form.set_all_readonly(False) # allow changing the .value of all controls
    print "the event, ", "Page$"+pageasstr
    #javascript:__doPostBack('GridView1','Page$3')
    br['__EVENTTARGET'] = 'GridView1'
    br['__EVENTARGUMENT'] = "Page$"+pageasstr
    response = br.submit()
    html2 = response.read()
    print "Page %d page length %d" % (pagenum, len(html2))
    #print html
    for csv in re.findall(">.*.CSV", html2):
        print "CSV:", csv
    
    
