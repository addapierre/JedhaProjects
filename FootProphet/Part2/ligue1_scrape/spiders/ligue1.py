import scrapy
import pandas as pd
import numpy as np
import re


################################################################################################################################################
################################################################################################################################################


class Ligue1Spider(scrapy.Spider):
    name = 'ligue1'
    start_urls = ['https://www.lequipe.fr/Football/ligue-1/page-participants']

    def parse(self, response):
        for link in response.css('li[pays="FRA"]'):

            
            yield response.follow('https://www.lequipe.fr'+link.css('a.link::attr(href)').get(), callback = self.parse_club)
    
    def parse_club(self, response):
        club_id = response.request.url
        club_id = re.search("[\d]+.html",club_id).group(0).replace('.html','')
        club = response.css('h1.nom_sportif::text').get()
        
        try:
            response.css('tr[role="row"] td.nom a::attr(title)').get().replace('la fiche de ','')
            for player in response.css('tr[role="row"]'):
                nom = player.css('td.nom a::attr(title)').get().replace('la fiche de ','')

                short_name = player.css('td.nom a::text').get().strip()+player.css('td.nom a strong::text').get().strip()
                short_name = short_name.replace('.','. ')

                num = player.css('td.numero::text').get().strip()

                DoB = player.css('td.ddn.js-age::text').get().strip()

                poste = player.css('td.poste span::text').get().strip()

                id = player.css('td.nom a::attr(href)').get()
                id = re.search("[\d]+.html",id).group(0).replace('.html','')

                yield {
                    'club' : club,
                    'club_id' : club_id,
                    'number': num,
                    'name' : nom,
                    'short_name' : short_name,
                    'DoB' : DoB,
                    'poste' : poste,
                    'lequipe_id' : id
                }
        except:
            try:
                print(f'\n\npetit soucis avec {club}\n\n')
                for player in response.css('section.Palmares.effectifclub tr.alternate1'):
                    nom =player.css('td.nom strong::text').get()
                    
                    DoB = player.css('td.ddn::text').get()
                    poste = player.css('td.poste::text').get()
                    
                    yield {
                        'club':club,
                        'name':nom,
                        'DoB' : DoB,
                        'poste':poste,
                        
                    }
                
                for player in response.css('section.Palmares.effectifclub tr.alternate2'):
                    nom =player.css('td.nom strong::text').get()
                    
                    DoB = player.css('td.ddn::text').get()
                    poste = player.css('td.poste::text').get()
                    
                    yield {
                        'club':club,
                        'name':nom,
                        'DoB' : DoB,
                        'poste':poste,
                        
                    }
            except:
                print('\n\nNOOOOONNONONNNNNNOOOON'+club+'\n\n')


    

################################################################################################################################################
################################################################################################################################################


class Ligue1Games(scrapy.Spider):
    name = 'ligue1_allgames'
    
    start_urls = ['https://www.lequipe.fr/Football/ligue-1/page-calendrier-resultats']
    

    def parse(self, response):
        
        for i in range(1,23):
            if i ==1:
                yield response.follow(self.start_urls[0]+'1re-journee', callback = self.parse_journee)
            else:
                yield response.follow(self.start_urls[0]+str(i)+'e-journee', callback = self.parse_journee)

            

    def parse_journee(self, response):
        try:
            self.journee = response.css('div.SelectNav__label.icon.icon--arrowDown::text').get()
            self.journee = re.search(r'^\d*',self.journee).group(0)
        except:
            print('\n\nprobleme\n\n')
            self.journee = -1

        for game in response.css('div.TeamScore'):
            self.home_goals = -1
            self.away_goals = -1
            self.home_club_id = -1
            self.away_club_id = -1
            self.game_id = -1
            try:
                
                
                clubs_url = game.css('a.TeamScore__team::attr(href)').getall()                              
                self.home_club_id = re.search("[\d]+.html",clubs_url[0]).group(0).replace('.html','')        ###
                self.away_club_id = re.search("[\d]+.html",clubs_url[1]).group(0).replace('.html','')        ###
                score = game.css('div.TeamScore__score span::text').getall()
                self.home_goals = score[0]                                                              ###                             
                self.away_goals = score[-1]                                                             ###
                game_url =  game.css('div.TeamScore__data a.Link::attr(href)').get()
                self.game_id = re.search( '\d+$' ,game_url).group(0)                                    ###
                yield {
                    'journee': self.journee,
                    'game_id': self.game_id,
                    'home_club_id' : self.home_club_id,
                    'away_club_id' : self.away_club_id,
                    'home_goals' : self.home_goals,
                    'away_goals' : self.away_goals
                }
            except:
                print(f'\n\n{self.journee}e journee')
                try:
                    print('home club',self.home_club_id,'away_club',self.away_club_id)
                    try:
                        print(self.home_goals,self.away_goals, self.game_id ,'\n\n')
                    except:
                        pass
                except:
                    pass
    

    


################################################################################################################################################
################################################################################################################################################


class Ligue1PlayerPosition(scrapy.Spider):
    name = 'ligue1_player_position'
    
    start_urls = ['https://www.lequipe.fr/Football/ligue-1/page-calendrier-resultats/']

    def parse(self, response):
        self.journee = response.css('div.SelectNav__label.icon.icon--arrowDown::text').get()
        self.journee = int(re.search(r'^\d+',self.journee).group(0))
        for game in response.css('div.TeamScore'):
            game_url = game.css('div.TeamScore__data a.Link::attr(href)').get()
            yield response.follow(game_url, callback = self.parse_game)
 

    def parse_game(self, response):

        try:
            clubs = response.css('a.Link.TeamScore__team::attr(href)').getall()
            home_club_id = int(re.search('\d+.html',clubs[0]).group(0).replace('.html',''))
            away_club_id = int(re.search('\d+.html',clubs[1]).group(0).replace('.html',''))
            

            game_id = response.request.url
            game_id = int(re.search(r'\d+$',game_id).group(0))
            print(f'\n{game_id}\n')
        except:
            print('\n\n Problem getting basic info\n\n')
        
        try:
            i=0
            for i,player in enumerate(response.css('div.field__content div.fieldPlayer')):
                position = player.css('div.fieldPlayer.fieldPlayer--positionned::attr(style)').get()
                number = int(player.css('span.fieldPlayer__value::text').get())
                name = player.css('span.fieldPlayer__title::text').get()
                if i<11:
                    yield {
                        'journee'   : self.journee,
                        'game_id'   : game_id,
                        'club_id'   : home_club_id,
                        'number'    : number,
                        'name'      : name,
                        'field_pos' : position
                    }
                else:
                    yield {
                        'journee'   : self.journee,
                        'game_id'   :game_id,
                        'club_id'   : away_club_id,
                        'number'    : number,
                        'name'      : name,
                        'field_pos' : position
                    }
        except:
            print(f'\n\n Problem with game {self.game_id} \n\n')

        








################################################################################################################################################
################################################################################################################################################

class Ligue1SofifaGK(scrapy.Spider):
    name = 'sofifa_GK'
    
    start_urls = ['https://sofifa.com/']


    def parse(self, response):

        sofifa_df = pd.read_csv('/Users/pierreadda/Documents/Jedha_projects/foot_scraping/ligue1/data/players_sofifa.csv', \
        usecols= ['sofifa_id', 'poste'],)
        
        sofifa_list = sofifa_df.loc[(~sofifa_df.sofifa_id.isnull()) & ( sofifa_df.poste == 'Gar.' )\
                , 'sofifa_id'].values.astype(np.int32)
        
        for sofifa in sofifa_list:
            player_url = 'https://sofifa.com/player/' + str(sofifa)
            yield response.follow(player_url, callback = self.parse_player)

    def parse_player(self, response):
        sofifa_id = response.css('li.ellipsis::text').getall()[-1]
        try:
            GK_stats_col = np.asarray(['sofifa_id', 'overall' ,'potential','attacking_crossing','attacking_heading_accuracy','skill_curve','skill_fk_accuracy', 
                'movement_agility','movement_reactions', 'movement_balance', 'power_shot_power','power_jumping', 'power_stamina',
                'mentality_aggression','mentality_positioning', 'mentality_penalties','goalkeeping_diving', 
                'goalkeeping_speed'])

            stats = np.asarray(response.css('span.bp3-tag.p::text').getall()).astype(np.int8)
            stats = stats[[0,1,5,7,11,12, 17, 18, 19, 20, 21, 22, 25, 27, 29, 34]] #select only the relevant stats
            
            GK_speed = response.css('body.is-preload script').getall()[1]
            GK_speed = np.int8(re.search('POINT_DEF=\d+',GK_speed).group(0).replace('POINT_DEF=',''))
            stats = np.append(stats,GK_speed)

            stats = np.append(np.asarray([sofifa_id]),stats)

            yield{
                     x[0] : x[1] for x in zip(GK_stats_col,stats)   
                    }

        except:
            print(f'\n{sofifa_id}\n')

 
################################################################################################################################################
################################################################################################################################################

class Ligue1SofifaAll(scrapy.Spider):
    name = 'sofifa_players'
    
    start_urls = ['https://sofifa.com/']


    def parse(self, response):

        sofifa_df = pd.read_csv('/Users/pierreadda/Documents/Jedha_projects/foot_scraping/ligue1/data/players_sofifa.csv', \
        usecols= ['sofifa_id', 'poste'],)
        
        sofifa_list = sofifa_df.loc[(~sofifa_df.sofifa_id.isnull()) & ( sofifa_df.poste != 'Gar.' )\
                , 'sofifa_id'].values.astype(np.int32)
        
        for sofifa in sofifa_list:
            player_url = 'https://sofifa.com/player/' + str(sofifa)
            yield response.follow(player_url, callback = self.parse_player)

    def parse_player(self, response):
        sofifa_id = int(response.css('li.ellipsis::text').getall()[-1])
        try:
            stats_col = np.asarray(['sofifa_id', 'overall' ,'potential','weak_foot', 'skill_moves', 'international_reputation', 'pace', 'shooting', \
                'passing', 'dribbling', 'defending', 'physic','attacking_crossing','attacking_heading_accuracy','skill_curve','skill_fk_accuracy', 'movement_agility',\
                    'movement_reactions', 'movement_balance', 'power_shot_power','power_jumping', 'power_stamina','mentality_aggression',\
                        'mentality_positioning', 'mentality_penalties','mentality_composure'])

            stats = np.asarray(response.css('span.bp3-tag.p::text').getall()).astype(np.int8)
            stats = stats[[0, 1, 5, 7, 11, 12, 17, 18, 19, 20, 21, 22, 25, 27, 29, 30]] #select only the relevant stats
            
            stats_gen = response.css('body.is-preload script').getall()[1]
            stats_gen = np.asarray(re.findall(r'POINT_\w+=(\d+)',stats_gen)).astype(np.int8)

            stats_star = np.asarray(response.css('li.ellipsis::text').getall())[[1,3,5]].astype(np.int8)

            stats_final = np.append(np.asarray([sofifa_id]),stats[:2])
            stats_final = np.append(stats_final,stats_star)
            stats_final = np.append(stats_final,stats_gen)
            stats_final = np.append(stats_final,stats[2:])


            yield{
                     x[0] : x[1] for x in zip(stats_col,stats_final)   
                    }

        except:
            print(f'\n{sofifa_id}\n')





################################################################################################################################################
################################################################################################################################################


