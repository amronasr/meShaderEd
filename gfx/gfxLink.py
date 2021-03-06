#===============================================================================
# gfxLink.py
#
# 
#
#===============================================================================
import os, sys
from PyQt4 import QtCore, QtGui
#
# GfxLink
#
class GfxLink ( QtGui.QGraphicsItem ):
  Type = QtGui.QGraphicsItem.UserType + 2 
  isStraight = True
  #
  #
  @staticmethod
  def createFromPoints ( srcP, dstP ):
    gfxLink = GfxLink ()
    gfxLink.srcPoint = gfxLink.mapToItem ( gfxLink, srcP )
    gfxLink.dstPoint = gfxLink.mapToItem ( gfxLink, dstP )
    gfxLink.adjust ()
    
    return gfxLink
  #
  #
  @staticmethod
  def createFromLink ( link ):
    gfxLink = GfxLink ()
    gfxLink.link = link
    gfxLink.path = QtGui.QPainterPath ()            
    gfxLink.adjust ()
    
    return gfxLink
  #
  #
  def __init__ ( self, link = None, srcConnector = None, dstConnector = None ):
    QtGui.QGraphicsItem.__init__ ( self )
    self.isStraight = True
    
    # qt graphics stuff
    self.brushSelected = QtGui.QBrush ( QtGui.QColor ( 250, 250, 250 ) )
    self.brushNormal = QtGui.QBrush ( QtGui.QColor ( 20, 20, 20 ) ) 
    self.setFlag ( QtGui.QGraphicsItem.ItemIsSelectable )
    self.setZValue( 0 )           
    
    self.link = link

    self.rect = QtCore.QRectF()
    self.points = []
    self.path = None
    self.isLinkSelected = False
    self.srcPoint = self.dstPoint = None
    self.srcConnector = self.dstConnector = None

    self.setSrcConnector( srcConnector )
    self.setDstConnector( dstConnector)
  #
  #
  def __delete__ ( self, instance ) :
    print ">> delete gfxLink"
  #
  #
  def remove ( self ) :
    print ">>GfxLink remove gfxLink"
    
    if self.srcConnector is not None : 
      self.srcConnector.removeLink( self )
      #self.srcConnector = None
    if self.dstConnector is not None : 
      self.dstConnector.removeLink( self )
      #self.dstConnector = None
    #if self.link is not None :
    scene = self.scene() 
    if scene != None :  
      scene.emit ( QtCore.SIGNAL( "onGfxLinkRemoved" ), self )
  #
  #
  def type ( self ): return GfxLink.Type
  #
  #
  def boundingRect ( self ): return self.rect
  #
  #
  def shape ( self ): return self.path 
  #
  #
  def swapConnectors ( self ): 
    # swap source and destination
    src = self.srcConnector
    self.srcConnector = self.dstConnector
    self.dstConnector = src
  #
  #
  def isDstConnectedTo ( self, connector ): 
    connected = False
    if connector == self.dstConnector :
      connected = True      
    return connected 
  #
  #
  def isEqual ( self, link ): 
    equal = False
    if self.srcConnector == link.srcConnector and self.dstConnector == link.dstConnector :
      equal = True
    elif self.srcConnector == link.dstConnector and self.dstConnector == link.srcConnector :  
      equal = True      
    return equal 
  #
  #
  def setSrcConnector ( self, srcConnector ): 
    if srcConnector is not None : 
      self.srcPoint = srcConnector.getCenterPoint()   
      self.srcConnector = srcConnector
      self.srcConnector.addLink ( self ) 
  #
  #
  def setDstConnector ( self, dstConnector ): 
    if dstConnector is not None : 
      self.dstPoint = dstConnector.getCenterPoint()   
      self.dstConnector = dstConnector
      self.dstConnector.addLink ( self ) 
  #
  #
  def itemChange ( self, change, value ):
    if change == QtGui.QGraphicsItem.ItemSelectedChange:
      self.isLinkSelected = value.toBool()
    
    return QtGui.QGraphicsItem.itemChange ( self, change, value )   
  #
  #
  def setPoints ( self, srcP, dstP ):
    self.srcPoint = self.mapToItem ( self, srcP )
    self.dstPoint = self.mapToItem ( self, dstP )
    self.adjust()
  #
  #
  def setSrcPoint ( self, p ):
    self.srcPoint = self.mapToItem ( self, p )
    self.adjust()
  #
  #
  def setDstPoint ( self, p ):
    self.dstPoint = self.mapToItem ( self, p )
    self.adjust()
  #
  #
  def adjust ( self ):
    if self.srcConnector is not None : self.srcPoint = self.srcConnector.getCenterPoint()        
    if self.dstConnector is not None : self.dstPoint = self.dstConnector.getCenterPoint()

    self.prepareGeometryChange()
    
    del self.points[:]  # clear bezier points
    self.path = None
    if self.srcPoint is not None and self.dstPoint is not None :
      self.path = QtGui.QPainterPath ()
      self.points.append ( self.srcPoint )
      self.path.moveTo ( self.points[ 0 ] )
      if not self.isStraight :
        pass
      self.points.append ( self.dstPoint ) 
      self.path.lineTo ( self.points[ -1 ] )
      self.rect = self.path.boundingRect()
  #
  #
  def adjust_old ( self, computeFromGfxNodes = False ):
    if computeFromGfxNodes:
      sourceP = self.link.sourceNode.gfxNode.pointFromProperty ( self.link.sourceProp )
      self.sourcePoint = self.mapToItem(self, sourceP)
      destP = self.link.destNode.gfxNode.pointFromProperty ( self.link.destProp )
      self.destPoint = self.mapToItem ( self, destP )
    
    # clear bezier points
    self.points = []
        
    self.prepareGeometryChange()
            
    # hull spline
    hull = QtCore.QRectF (self.sourcePoint, self.destPoint )
    centerX = hull.center().x()
    centerY = hull.center().y()

    # first 
    self.points.append(self.sourcePoint)
    
    # second point
    offsetVX = abs((hull.topRight().x() - hull.topLeft().x()) * 0.35)
    offsetVY = 0.0
    
    secondP = self.sourcePoint + QtCore.QPointF(offsetVX, offsetVY)
    self.points.append(secondP)
    
    # third point
    thirdPX =  centerX
    thirdPY = self.sourcePoint.y()
    self.points.append(QtCore.QPointF(thirdPX, thirdPY))
    
    # fourth point
    self.points.append(QtCore.QPointF(centerX, centerY))
    
    # fifth point (bezier tangent)
    self.points.append(QtCore.QPointF(centerX, centerY))

    # sixth point
    sixthPX =  centerX
    sixthPY = self.destPoint.y()
    self.points.append(QtCore.QPointF(sixthPX, sixthPY))
    
    # seventh point
    seventhP = self.destPoint - QtCore.QPointF(offsetVX, offsetVY)
    self.points.append(seventhP)
    
    # last
    self.points.append(self.destPoint)
    
    # bezier curve path
    self.path = QtGui.QPainterPath()
    self.path.moveTo ( self.points[0] )
    self.path.cubicTo ( self.points[1], self.points[2], self.points[3] )
    self.path.cubicTo ( self.points[5], self.points[6], self.points[7] )
    
    # arrow
    arrowSize = 3
    if hull.topRight() == self.destPoint:
      arrowAnchor = hull.topRight()
    else:
      arrowAnchor = hull.bottomRight()
        
    firstArrowP = arrowAnchor 
    secondArrowP = QtCore.QPointF ( arrowAnchor.x() - arrowSize, arrowAnchor.y() - arrowSize )
    thirdArrowP = QtCore.QPointF ( arrowAnchor.x() - arrowSize, arrowAnchor.y() + arrowSize )
    fourthArrowP = arrowAnchor
    
    arrow = QtGui.QPolygonF ( [firstArrowP, secondArrowP, thirdArrowP, fourthArrowP] )
    self.path.addPolygon ( arrow )
    
    # rect
    self.rect = self.path.boundingRect()
  #
  #
  def paint ( self, painter, option, widget ):        
    if self.path is not None :
      painter.setRenderHint ( QtGui.QPainter.Antialiasing )
      brush = self.brushNormal
      if self.isLinkSelected : brush = self.brushSelected
      painter.setPen( QtGui.QPen( brush, 
                                  1.25, 
                                  QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin 
                                ) 
                    )
      painter.drawPath ( self.path ) 
