#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.db import cDb

import os, re, urllib, string, xbmc

class cGuiElement:

    DEFAULT_FOLDER_ICON = 'icon.png'
    COUNT = 0

    def __init__(self):
        self.__sRootArt = cConfig().getRootArt()
        self.__sType = 'video'
        self.__sMeta = 0
        self.__sPlaycount = 0
        self.__sTrailerUrl = ''
        self.__sMetaAddon = cConfig().getSetting('meta-view')
        self.__sMediaUrl = ''
        self.__sTitle = ''
        self.__sTitleSecond = ''
        self.__sFileName = ''
        self.__sDescription = ''
        self.__sThumbnail = ''
        self.__sIcon = self.DEFAULT_FOLDER_ICON
        self.__sFanart = self.__sRootArt+'fanart.jpg'
        self.__aItemValues = {}
        self.__aProperties = {}
        self.__aContextElements = []
        self.__sSiteName = ''
        cGuiElement.COUNT += 1
        
    #def __len__(self): return self.__sCount
    
    def getCount(self): 
        return cGuiElement.COUNT

    def setType(self, sType):
        self.__sType = sType

    def getType(self):
        return self.__sType
     
    def setMetaAddon(self, sMetaAddon):
        self.__sMetaAddon = sMetaAddon

    def getMetaAddon(self):
        return self.__sMetaAddon
        
    def setTrailerUrl(self, sTrailerUrl):
        self.__sTrailerUrl = sTrailerUrl

    def getTrailerUrl(self):
        return self.__sTrailerUrl
        
    def setMeta(self, sMeta):
        self.__sMeta = sMeta

    def getMeta(self):
        return self.__sMeta

    def setMediaUrl(self, sMediaUrl):
        self.__sMediaUrl = sMediaUrl

    def getMediaUrl(self):
        return self.__sMediaUrl

    def setSiteName(self, sSiteName):
        self.__sSiteName = sSiteName

    def getSiteName(self):
        return self.__sSiteName
         
    def setFileName(self, sFileName):
        self.__sFileName = self.str_conv(sFileName)

    def getFileName(self):
        return self.__sFileName
        
    def setFunction(self, sFunctionName):
        self.__sFunctionName = sFunctionName

    def getFunction(self):
        return self.__sFunctionName

    def setTitle(self, sTitle):
        self.__sTitle = sTitle;

    def getTitle(self):
        return self.__sTitle

    def setTitleSecond(self, sTitleSecond):
        self.__sTitleSecond = sTitleSecond

    def getTitleSecond(self):
        return self.__sTitleSecond

    def setDescription(self, sDescription):
        self.__sDescription = sDescription

    def getDescription(self):
        return self.__sDescription

    def setThumbnail(self, sThumbnail):
        self.__sThumbnail = sThumbnail

    def getThumbnail(self):
        return self.__sThumbnail
    
    def setFanart(self, sFanart):
        self.__sFanart = sFanart

    def getFanart(self):
        return self.__sFanart

    def setIcon(self, sIcon):
        self.__sIcon = sIcon

    def getIcon(self):
        return self.__sRootArt+self.__sIcon

    def addItemValues(self, sItemKey, mItemValue):
        self.__aItemValues[sItemKey] = mItemValue
    
    def getWatched45(self):
        watched = {}
        count = 0
        watched_db = os.path.join( cConfig().getSettingCache(), "watched.db" )
        try: 
            if os.path.exists( watched_db ):
                watched = eval( open(watched_db).read() )
                sTitle = self.getTitle()
                sId = self.getSiteName()
                if sTitle in watched.get(sId):
                    count = 1
                else:
                    count = 0           
        except:
            return
        return count
        
    def getWatched(self):
        meta = {}      
        meta['title'] = urllib.quote_plus(self.getTitle())
        meta['site'] = self.getSiteName()
        data = cDb().get_watched(meta)
        return data   
    
        
    def setWatched(self, sId, sTitle):
        try:
            watched = {}
            #sTitle = self.getTitle()
            #sId = self.getSiteName()
            watched_db = os.path.join(cConfig().getSettingCache(), "watched.db" )
            
            if not os.path.exists(watched_db):
                file(watched_db, "w").write("%r" % watched) 

            if os.path.exists(watched_db):
                watched = eval(open(watched_db).read() )
                watched[ sId ] = watched.get( sId ) or []
                #add to watched
                if sTitle not in watched[sId]:
                     watched[ sId ].append( sTitle )
                else:
                    del watched[ sId ][ watched[ sId ].index( sTitle ) ]
            
            file(watched_db, "w").write("%r" % watched)
            watched_db.close()
        except:
            return

    
    def str_conv(self, data):
        if isinstance(data, str):
            # Must be encoded in UTF-8
            data = data.decode('utf8')
        
        import unicodedata
        data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
        data=re.sub(r'\[.*\]|\(.*\)',r'',str(data))
        data=data.replace('VF','').replace('VOSTFR','').replace('FR','')
        data=re.sub(r'[0-9]+?',r'',str(data))
        data=data.replace('-','').replace('Saison','').replace('saison','').replace('Season','').replace('Episode','').replace('episode','')
        data = re.sub('[^%s]' % string.ascii_lowercase, ' ', data.lower())
        #data = urllib.quote_plus(data)
        
        #data = data.decode('string-escape')
        
        return data
        
    def getInfoLabel(self):
        meta = {
        'title': xbmc.getInfoLabel('ListItem.title'), 
        'originaltitle': xbmc.getInfoLabel('ListItem.originaltitle'), 
        'year': xbmc.getInfoLabel('ListItem.year'), 
        'genre': xbmc.getInfoLabel('ListItem.genre'), 
        'director': xbmc.getInfoLabel('ListItem.director'), 
        'country': xbmc.getInfoLabel('ListItem.country'), 
        'rating': xbmc.getInfoLabel('ListItem.rating'), 
        'votes': xbmc.getInfoLabel('ListItem.votes'), 
        'mpaa': xbmc.getInfoLabel('ListItem.mpaa'), 
        'duration': xbmc.getInfoLabel('ListItem.duration'), 
        'trailer': xbmc.getInfoLabel('ListItem.trailer'), 
        'writer': xbmc.getInfoLabel('ListItem.writer'), 
        'studio': xbmc.getInfoLabel('ListItem.studio'), 
        'tagline': xbmc.getInfoLabel('ListItem.tagline'), 
        'plotoutline': xbmc.getInfoLabel('ListItem.plotoutline'), 
        'plot': xbmc.getInfoLabel('ListItem.plot'),
        'cover_url': xbmc.getInfoLabel('ListItem.Art(thumb)'),
        'backdrop_url': xbmc.getInfoLabel('ListItem.Art(fanart)')
        }
        
        if meta['title']:
            meta['title'] = self.getTitle()
            
        for key, value in meta.items():
            self.addItemValues(key, value)
        
        if meta['backdrop_url']:
            self.addItemProperties('fanart_image', meta['backdrop_url'])
            self.__sFanart = meta['backdrop_url']
        if meta['trailer']:
            meta['trailer'] = meta['trailer'].replace(u'\u200e', '').replace(u'\u200f', '')
            self.__sTrailerUrl = meta['trailer']
        if meta['cover_url']:
            self.__sThumbnail = meta['cover_url']
        
        return
    def getMetadonne(self):
        from metahandler import metahandlers
        grab = metahandlers.MetaData(preparezip=False)
        #sTitle = self.__sTitle.decode('latin-1').encode("utf-8")
        #sTitle=re.sub(r'\[.*\]|\(.*\)',r'',str(self.__sFileName))
        #sTitle=sTitle.replace('VF','').replace('VOSTFR','').replace('FR','')

        if self.getMeta() == 1:
            meta = grab.get_meta('movie',self.__sFileName)
        elif self.getMeta() == 2:
            #sTitle=re.sub(r'[0-9]+?',r'',str(sTitle))
            #sTitle=sTitle.replace('-','').replace('Saison','').replace('saison','').replace('Season','').replace('Episode','').replace('episode','')
            meta = grab.get_meta('tvshow',self.__sFileName)
        else:
            return
        del meta['playcount']
               
        if meta['title']:
            meta['title'] = self.getTitle()
            
        for key, value in meta.items():
            self.addItemValues(key, value)
         
        if meta['backdrop_url']:
            self.addItemProperties('fanart_image', meta['backdrop_url'])
            self.__sFanart = meta['backdrop_url']
        if meta['trailer_url']:
            meta['trailer'] = meta['trailer'].replace(u'\u200e', '').replace(u'\u200f', '')
            self.__sTrailerUrl = meta['trailer']
        if meta['cover_url']:
            self.__sThumbnail = meta['cover_url']
        return

    def getItemValues(self):
        self.__aItemValues['Title'] = self.getTitle()
        self.__aItemValues['Plot'] = self.getDescription()
        self.__aItemValues['Playcount'] = self.getWatched()
        self.addItemProperties('fanart_image', self.__sFanart)
        

        if self.getMeta() > 0 and self.getMetaAddon() == 'true':
            self.getMetadonne()
        return self.__aItemValues
    
    def addItemProperties(self, sPropertyKey, mPropertyValue):
        self.__aProperties[sPropertyKey] = mPropertyValue

    def getItemProperties(self):
        return self.__aProperties

    def addContextItem(self, oContextElement):
        self.__aContextElements.append(oContextElement)

    def getContextItems(self):
        return self.__aContextElements

