import pandas as pd
from selectolax.parser import HTMLParser
import httpx


re_strip = lambda sp,st : sp.join(re.findall('\S+',st)) # function for normal regex by finding all char

class Match:


    def __init__(self,node) -> None:
        self.match_url = 'https://www.vlr.gg' + node.attributes['href']
        self.html = HTMLParser(httpx.get(self.match_url).text)
        
        match_name = self.html.css_first('title').text().strip().split(' | ')[0].split(' vs. ')
        
        messy_match_result = self.html.css_first('div.js-spoiler').text()
        match_result = ' ' + re_strip('',messy_match_result) + ' '
        
        self.match_sum = match_result.join(match_name)
        
        self.stage = re_strip(' ',self.html.css_first('div.match-header-event-series').text())
        
        # self.ban_pick = re_strip(' ',self.html.css_first('div.match-header-note').text()).split('; ')
        self.ban_pick = None if (h:=self.html.css_first('div.match-header-note')) is None\
        else re_strip(' ',h.text()).split('; ')
        
        self.date = re_strip(' ',self.html.css_first('div.match-header-date').text())
        
        
    def __repr__(self):
        return self.match_sum
    
    def _extract_data(self,data):
        try:
            list_data = re.findall('[\d+-.]+',data)
            if (ll:=len(list_data)) == 0:
                return 'Nan Nan Nan'
            elif ll < 3:
                list_data += ['0'] * (3-ll)
            return ' '.join(list_data)
        except TypeError:
            return f'{data} Nan Nan'
        
    def _extract_df(self,df):
        filled_df =df.fillna('Nan Nan Nan').astype('object')
    
        name = filled_df.iloc[:,0].map(lambda s : s.split(' ')[0])
        team = filled_df.iloc[:,0].map(lambda s : s.split(' ')[1])

        filled_df.iloc[:,0] = name
        filled_df.iloc[:,1] = team

        formatted_df = filled_df.rename(columns={'Unnamed: 0':'Name','Unnamed: 1':'Team'})



        # formatted_df.iloc[:,2:] = formatted_df.iloc[:,2:].applymap(lambda x :  ' '.join(re.findall("[\d+-.]+",x,re.A)))
        formatted_df.iloc[:,2:] = formatted_df.iloc[:,2:].applymap(self._extract_data)



        new_columns = []
        for c in formatted_df.columns[2:]:
            for side in ['all','atk','def']:
                new_columns.append((c,side))

        new_columns = np.array(new_columns).reshape(-1,3,2)


        result_df = pd.DataFrame(formatted_df.iloc[:,:2])


        result_df.columns = [('Name','Name'),('Team','Team')]


        for nc,c in zip(new_columns,formatted_df.iloc[:,2:].columns):
            result_df[list(map(lambda x: tuple(x),list(nc)))] = formatted_df[c].str.split(' ',expand=True)


        result_df.columns = pd.MultiIndex.from_tuples(result_df.columns,name=['Type','Side'])

        return result_df
        
        
    
    def get_scoreboard(self):
        result = {}
        maps = self.html.css('div.vm-stats-game')
          # extract data of each map
        for m in maps:
            # get the current map pick name or overall if it the match summary
            current_map = m.css_first('div.map')
            match_header = 'Overall' if not current_map else\
                            ' '.join(re_strip(' ',current_map.text()).split(' ')[::2])

            print(match_header)


            tables = m.css('table.wf-table-inset')

            for table in tables:
                df = pd.read_html(table.html)[0]
                result[match_header] = self._extract_df(df)
                
        return result
