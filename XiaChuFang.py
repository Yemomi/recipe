# coding=utf-8
from bs4 import BeautifulSoup
from urllib import urlopen
import urllib
import json
import os

#webdata = urlopen("http://www.xiachufang.com/recipe/000000001/").read();

#生成url
def createUrl(originUrl,index): 

	return originUrl + "%d"%index;

def findObjectOfSoupTagKindByClassName(soup,tagKind,className):

	return soup.find_all(tagKind,class_=className);

#----------------获取食谱信息函数集---------------------
	#菜品名
def getNameof(soup):
	name = findObjectOfSoupTagKindByClassName(soup,"h1","page-title");

	#print "+++++++++++++++++++++++++++";
	#print name;
	#print name[0].contents[0].strip();
	return name[0].contents[0].strip();

	#菜品分类
def getRecipeCatof(soup):
	recipeCat = findObjectOfSoupTagKindByClassName(soup,"div","recipe-cats");

	#print recipeCat[0].contents[1].contents[0];
	return recipeCat[0].contents[1].contents[0];

	#菜品简介
def getBriefIntroduceof(soup):
	desc = soup.find_all("div", class_='desc');
	#print desc[0].contents[0].encode('utf8');

	#print desc[0].contents[0].strip();
	return desc[0].contents[0].strip();

	#菜品用料名
def getIngredientsNameOf(soup):
	ingredientsName = findObjectOfSoupTagKindByClassName(soup,"td","name has-border");
	ingredientsNameArray = [];

	#print len(ingredientsName);
	for index in xrange(0,len(ingredientsName)):
		#print ingredientsName[index].contents;
		tempIgN = ingredientsName[index].contents;
		if len(tempIgN) > 1:
			#print tempIgN[1].get_text();
			ingredientsNameArray.append(tempIgN[1].get_text());
		else:
			#print tempIgN[0].strip();
			ingredientsNameArray.append(tempIgN[0].strip());		

	#print "length of array : %d"%len(ingredientsNameArray);
	#print ingredientsNameArray;
	return ingredientsNameArray;

	#菜品用料数
def getIngredientsUnitof(soup):
	ingredientsUnit = findObjectOfSoupTagKindByClassName(soup,"td","unit has-border");
	ingredientsUnitArray = [];

	for index in xrange(0, len(ingredientsUnit)):
		ingredientsUnitArray.append(ingredientsUnit[index].contents[0].strip());
		#print ingredientsUnitArray[index];

	return ingredientsUnitArray;

	#菜品制作步骤
def getStepsOf(soup):
	steps = findObjectOfSoupTagKindByClassName(soup,"li","container");
	#print steps;
	stepsArray = [];
	for index in xrange(0,len(steps)):
		stepsArray.append(steps[index].contents[1].get_text());
		#print stepsArray[index];

	return stepsArray;

	#获得菜品图片url
def getCoverImgUrlOf(soup):
	orginImgUrl = findObjectOfSoupTagKindByClassName(soup,"div","cover image expandable block-negative-margin");
	tempStr = str(orginImgUrl[0]);
	pre = tempStr.index('(')+1;
	last = tempStr.index(')');
	imgUrl = tempStr[pre:last];
	#print imgUrl;
	#print pre;
	#print last;
	imgname = getNameof(soup);
	downloadImgbyUrl(imgUrl, imgname);

	#aft = imgUrl[0].find(")");
	#t = imgUrl[0][pre,aft];
	#print imgUrl;

	return imgUrl
#----------------------------------------------------

def downloadImgbyUrl(url,imgfilename):
	filepath = "/Users/yewenjian/Documents/Img/" + imgfilename + ".jpg";
	#print filepath;
	urllib.urlretrieve(url, filepath);
#---------------信息处理函数---------------------------
def getAllRecipeInfoof(soup):
	recipeName = getNameof(soup);
	recipeCat  = getRecipeCatof(soup);
	recipeIndr = getBriefIntroduceof(soup);
	recipeIngN = getIngredientsNameOf(soup);
	recipeIngU = getIngredientsUnitof(soup);
	recipeStep = getStepsOf(soup);
	#recipeImgUrl = getCoverImgUrlOf(soup);

	recipeInfoDictionary = {'name':recipeName,
							'cat' :recipeCat,
							'ingredient':{"ingredientName":recipeIngN, "ingredientUnit":recipeIngU},
							'steps':recipeStep
							};

	print recipeInfoDictionary;

	return recipeInfoDictionary;
#-----------------------------------------------------
def getDestionFilePathbyFileName(fileName):
	return os.path.abspath('..') +"/Documents/Recipe/" + fileName + '.json';

def arrayFormater(originArray):
	arrayToString = "[";
	for item in originArray:
		arrayToString += "\""+item + "\",";
	arrayToString = arrayToString[0:-1]
	arrayToString += "]";
	#print arrayToString;
	return arrayToString;

def createJsonFileofHtml(soup):
	#recipeInfoDictionary = getAllRecipeInfoof(soup);
	#获得食谱信息
	recipeName = getNameof(soup);
	#recipeCat  = getRecipeCatof(soup);
	recipeIndr = getBriefIntroduceof(soup);
	recipeIngN = getIngredientsNameOf(soup);
	recipeIngU = getIngredientsUnitof(soup);
	recipeStep = getStepsOf(soup);
	recipeImgUrl = getCoverImgUrlOf(soup);


	#print arrayFormater(recipeIngN);
	#打开目的文件
	Destinationfile = open(getDestionFilePathbyFileName(recipeName),'w');
	#写入信息
	fileContent = "{\"name\":\"" + recipeName + "\",";
	fileContent += "\"getBriefIntroduce\":\"" + recipeIndr + "\",";
	#fileContent += "\"kind\":\"" + recipeCat + "\",";
	fileContent += "\"ingredients\":{\"ingredientName\":" + arrayFormater(recipeIngN) + "," + "\"IngredientUnit\":" + arrayFormater(recipeIngU) + "},";
	fileContent += "\"steps\":" + arrayFormater(recipeStep) + ",";
	fileContent += "\"imgUrl\":\"" + recipeImgUrl + "\"}"

	#print "------------------------------"
	#print fileContent.encode('utf-8');
	Destinationfile.write(fileContent.encode('utf-8'));
	#关闭目的文件
	Destinationfile.close();

originUrl = "http://www.xiachufang.com/recipe/";

	#遍历目标地址
for x in xrange(264,600):
	if x != 134:
			#生成目标url
		recipeUrl = createUrl(originUrl,x);
		
		#获得html文档并转换为soup格式
		webdata   = urlopen(recipeUrl);
		soup      = BeautifulSoup(webdata);

		#getCoverImgUrlOf(soup);
		percentage = x*100;
		percentage = percentage/600;
		print "percentage:%d"%percentage+"%";
		#获得食谱信息
		createJsonFileofHtml(soup);

		#getCoverImgUrlOf(soup);







