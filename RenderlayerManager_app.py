import maya.cmds
import maya.mel as mel

class renderLayerMan_UI(object):

	_AppVersion_ = '1.0B'

	def __init__(self):
		pass

	def delete_renderLayer( self, name='', *args ):
		try :
			cmds.delete(name)
		except :
			cmds.button('button_delete_' + name, e = True, l = 'layer is in used.', backgroundColor = (1,0,0) , en = False )
			cmds.error('Render layer ' + name + ' is in use.' )
		print( '>> ' + name + ' was delete.' )
		self.update_layerList()

	def update_layerList( self ):
		''' Description '''

		for child in cmds.formLayout( 'renderLayerman_mainForm' , q=True, ca=True ) or [] :
			cmds.deleteUI( child )
		cmds.setParent( 'renderLayerman_mainForm' )

		new_row = cmds.rowColumnLayout( numberOfColumns = 5, rs= (1,3), columnWidth = [ (1,10),(2,25),(3, 150), (4, 5), (5, 100) ] )
		for renderLayer in cmds.ls( type = 'renderLayer' ):
			button_en = True
			#print renderLayer

			if 'defaultRenderLayer' in renderLayer :
				button_en = False

			focus_button_cmd = 'renderLayerMan_UI().Button_focus_onclick( name = \'{0}\' )'.format( renderLayer ) 
			cmds.button(l='>' ,en=button_en, command = focus_button_cmd ) 
			setting_button_cmd = 'renderLayerMan_UI().Button_setting_onClick( name = \'{0}\' )'.format( renderLayer ) 
			cmds.iconTextButton(  image1='gear.xpm', label='sphere' , command=setting_button_cmd)
			cmds.text( l = renderLayer )
			cmds.separator()
			button_cmd = 'renderLayerMan_UI().delete_renderLayer( name = \'{0}\' )'.format( renderLayer ) 
			cmds.button('button_delete_'+renderLayer ,l='delete' ,en=button_en, command = button_cmd ) 

		cmds.setParent('..')

		cmds.formLayout( 'renderLayerman_mainForm' , e = True, af = [(new_row,'top',0), (new_row, 'bottom', 0 ), (new_row,  'left', 0 ), (new_row, 'right', 0)])
		print( '>> Layer list was updated.' )

	def Button_ok_onClick( self, *args ) :
		''' description '''

		cmds.deleteUI( 'renderLayerMan' )

	def Button_focus_onclick(self, name, *args):
		''' description '''

		#--------------------------------
		#cmds.select(name)

		mel.eval ( ' showEditorExact(" ' + name + ' ") ' )
		print ('>> select \''+ name +'\'')


	def Button_setting_onClick( self, name, *args):
		''' Description '''

		cmds.editRenderLayerGlobals( currentRenderLayer = name )
		cmds.showWindow('unifiedRenderGlobalsWindow')

	def showUI( self ):
		''' Description '''

		#Delete Ould UI
		if cmds.window( 'renderLayerMan', ex= True ) :
			cmds.deleteUI( 'renderLayerMan' )


		cmds.window( 'renderLayerMan',w = 255 )
		UI_mainLayout = cmds.columnLayout( 'renderLayerman_mainLayout', adj = True, w = 295, h = 350 )

		cmds.columnLayout( 'renderLayerman_Content', rs=3, adj = True, parent = UI_mainLayout )

		cmds.rowLayout(numberOfColumns = 2, columnAlign=[ (1,'left') , (2,'right')], adj=True)
		cmds.text( l = 'Render layer manager' )
		focus_button_cmd = 'renderLayerMan_UI().update_layerList()' 
		cmds.iconTextButton(  image1='refresh.xpm', label='sphere' , command= focus_button_cmd)
		cmds.setParent('..')

		cmds.formLayout ( 'renderLayerman_mainForm' )

		self.update_layerList() 
		cmds.setParent('..')
		cmds.button( l = 'OK', command = self.Button_ok_onClick )
		cmds.separator(h=10)
		cmds.text('version_info', l= 'version : ' + self._AppVersion_ )
		cmds.setParent('..')
		
		cmds.showWindow( 'renderLayerMan' )


app = renderLayerMan_UI()
app.showUI()