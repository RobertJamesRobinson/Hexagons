import math
class Hexagon:
	# define the hexagon shape:
	# (like pygames rect)
	# a hexagon can be defined by its centre x,y, its radius and its orientation (long diameter vertical or horizontal)
	# a Hexagon can report its area as a list of integer pixel based points, given a center point
	
	def __init__(self,center,radius,orientation):
		self.radius=radius
		self.center=center
		self.orientation=orientation
		self.points=[]
		yOff=math.sin(math.pi/6)*radius
		xOff=math.cos(math.pi/6)*radius
		if orientation=="VERTICAL":
			self.points.append((int(center[0]-xOff),int(center[1]-yOff)))  #0, top left
			self.points.append((int(center[0]),int(center[1]-radius)))  #1, top
			self.points.append((int(center[0]+xOff),int(center[1]-yOff)))  #2, top right
			self.points.append((int(center[0]+xOff),int(center[1]+yOff)))  #3, bottom right
			self.points.append((int(center[0]),int(center[1]+radius)))  #4, bottom
			self.points.append((int(center[0]-xOff),int(center[1]+yOff)))  #5, bottom left
				
		if orientation=="HORIZONTAL":	
			self.points.append((int(center[0]-yOff),int(center[1]-xOff)))  #0, top left
			self.points.append((int(center[0]+yOff),int(center[1]-xOff)))  #1, top right
			self.points.append((int(center[0]+radius),int(center[1])))  #2, right
			self.points.append((int(center[0]+yOff),int(center[1]+xOff)))  #3, bottom right
			self.points.append((int(center[0]-yOff),int(center[1]+xOff)))  #4, bottom left
			self.points.append((int(center[0]-radius),int(center[1])))  #5, left
			
class HexTools:
	# this class supplies calculations for working with hexagonal game tiles
	# required functionality:
	# set a game size height and width (during initialisation) and individual tile radius and orientation, long diameter vertical or horizontal
	# if given an array index number, return an x,y board coordinate
	# if given an x,y board coordinate, return an array index number
	# if given a pixel based global xy, return a game tile xy
	# if given a game tile xy, return the global pixel based bounds of the hexagon in question
	
	#private attribute=None
	def __init__(self,boardSize,tileRadius=None,orientation=None):
		if tileRadius:
			self.boardWidth=boardSize[0]
			self.boardHeight=boardSize[1]
			self.tileRadius=tileRadius
			self.orientation=orientation
		else:
			self.boardWidth=boardSize.width
			self.boardHeight=boardSize.height
			self.tileRadius=boardSize.tileRadius
			self.orientation=boardSize.orientation
	
	
	def index2XY(self,index):
		# converts an 1D array index number to a tile index x and y coordinate
		result=None
		if index<self.boardWidth*self.boardHeight:
			result=(index%self.boardWidth,int(index/self.boardWidth))
		return result
	
	def XY2index(self,XY):
		#converts a tile index x and y coordinate to a 1D array index
		result=None
		if (XY[0]<self.boardWidth) and (XY[1]<self.boardHeight):
			result=self.boardWidth*XY[1]+XY[0]
		return result
		
	def XYPixel2XYBoard(self,XYPixel):
		#converts a global pixel based XY coordinate to a tile index x and y coordinate (must be a center point!)
		x=None
		y=None
		
		if self.orientation=="HORIZONTAL":
			const=math.cos(math.pi/6)*self.tileRadius
			x=(XYPixel[0]-self.tileRadius)/(self.tileRadius*1.5)
			y=(XYPixel[1]+(XYPixel[0]%2*const)-(2*const))/(2*const)
			return x,y
			
		if self.orientation=="VERTICAL":
			const=math.cos(math.pi/6)*self.tileRadius
			y=(XYPixel[1]-self.tileRadius)/(self.tileRadius*1.5)
			x=(XYPixel[0]-(XYPixel[1]%2*const)-(const))/(2*const)
			return x,y
		
		return None
	
	def nearestTile(self,XYPixel):
		#takes any pixel based coordinate and returns the board x and y coordinate indexs for the nearest tile
		best=None
		indexToTest=0
		best=self.index2XY(indexToTest)
		currentDistance=self.simpleDistance(XYPixel,self.XYBoard2XYPixel(self.index2XY(indexToTest)))
		#print self.boardWidth,self.boardHeight
		while indexToTest<(self.boardWidth*self.boardHeight-1):
			indexToTest+=1
			thisDistance=self.simpleDistance(XYPixel,self.XYBoard2XYPixel(self.index2XY(indexToTest)))
			if thisDistance<currentDistance:
				currentDistance=thisDistance
				best=self.index2XY(indexToTest)
		return best
			
	def simpleDistance(self,point1,point2):
		result=math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
		return result
	
	def XYBoard2XYPixelTopLeft(self,XYBoard):
		#converts a game X and Y index coordinate and returns the euclidean top left point of the pixel based tile, for placing square images onto tiles
		x=None
		y=None
		if self.orientation=="HORIZONTAL":
			const=math.cos(math.pi/6)*self.tileRadius
			#print XYBoard[0]
			x=XYBoard[0]*(self.tileRadius*1.5)+self.tileRadius
			y=XYBoard[1]*(2*const)+(2*const)-(XYBoard[0]%2*const)
			return x-self.tileRadius,y-const
		if self.orientation=="VERTICAL":
			const=math.cos(math.pi/6)*self.tileRadius
			y=XYBoard[1]*(self.tileRadius*1.5)+self.tileRadius
			x=XYBoard[0]*(const*2)+(const)+(XYBoard[1]%2*const)
			return x-const,y-self.tileRadius
		return None
		
		
	def XYBoard2XYPixelRect(self,XYBoard):
		#converts a game X and Y index coordinate and returns the euclidean Rect of the pixel based tile, for placing square images onto tiles
		x=None
		y=None
		if self.orientation=="HORIZONTAL":
			const=math.cos(math.pi/6)*self.tileRadius
			#print XYBoard[0]
			x=XYBoard[0]*(self.tileRadius*1.5)+self.tileRadius
			y=XYBoard[1]*(2*const)+(2*const)-(XYBoard[0]%2*const)
			return x-self.tileRadius,y-const,self.tileRadius*2,const*2
		if self.orientation=="VERTICAL":
			const=math.cos(math.pi/6)*self.tileRadius
			y=XYBoard[1]*(self.tileRadius*1.5)+self.tileRadius
			x=XYBoard[0]*(const*2)+(const)+(XYBoard[1]%2*const)
			return x-const,y-self.tileRadius,const*2,self.tileRadius*2
		return None
		
		
	def XYBoard2XYPixelBottomRight(self,XYBoard):
		#converts a game X and Y index coordinate and returns the euclidean top left point of the pixel based tile, for placing square images onto tiles
		x=None
		y=None
		if self.orientation=="HORIZONTAL":
			const=math.cos(math.pi/6)*self.tileRadius
			#print XYBoard[0]
			x=XYBoard[0]*(self.tileRadius*1.5)+self.tileRadius
			y=XYBoard[1]*(2*const)+(2*const)-(XYBoard[0]%2*const)
			return x+self.tileRadius,y+const
		if self.orientation=="VERTICAL":
			const=math.cos(math.pi/6)*self.tileRadius
			y=XYBoard[1]*(self.tileRadius*1.5)+self.tileRadius
			x=XYBoard[0]*(const*2)+(const)+(XYBoard[1]%2*const)
			return x+const,y+self.tileRadius
		return None
		
	def XYBoard2XYPixel(self,XYBoard):
		#converts a game tile X and y index coordinate and returns a global pixel based center point
		x=None
		y=None
		#if(XYBoard[0]<self.boardWidth and XYBoard[1]<self.boardHeight):
		if self.orientation=="HORIZONTAL":
			const=math.cos(math.pi/6)*self.tileRadius
			x=XYBoard[0]*(self.tileRadius*1.5)+self.tileRadius
			y=XYBoard[1]*(2*const)+(2*const)-(XYBoard[0]%2*const)
			return x,y
		if self.orientation=="VERTICAL":
			const=math.cos(math.pi/6)*self.tileRadius
			#print XYBoard
			y=XYBoard[1]*(self.tileRadius*1.5)+self.tileRadius
			x=XYBoard[0]*(const*2)+(const)+(XYBoard[1]%2*const)
			return x,y
		return None
		
		
	def XYBoard2HexList(self,XYBoard):
		#converts a game tile X and Y coordinate to the individual hexagons list of vertices
		result=Hexagon(self.XYBoard2XYPixel(XYBoard),self.tileRadius,self.orientation)
		return result.points