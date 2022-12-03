# Armadura 2
import openseespy.opensees as ops # Libreria de OpenSees
import vfo.vfo as vfo #Libreria para visualizar los modelos

# Se borrar modelos anteriores
ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)

# nodos
ops.node(1,0,3)
ops.node(2,4,2)
ops.node(3,4,0)
ops.node(4,8,3)

# restricciones
ops.fix(1,1,1)
ops.fix(4,0,1)

vfo.createODB(model= 'armp02')
vfo.plot_model(model= 'armp02', show_nodes='yes', show_nodetags= 'yes')

#materiales
tagMat=1
ops.uniaxialMaterial('Elastic', tagMat,20e8)

# elementos
A=1e-3
ops.element('truss',1,1,2,A,tagMat)
ops.element('truss',2,1,3,A,tagMat)
ops.element('truss',3,2,3,A,tagMat)
ops.element('truss',4,2,4,A,tagMat)
ops.element('truss',5,3,4,A,tagMat)

vfo.createODB(model='armp02', loadcase='Estatico')
vfo.plot_model(model='armp02', show_nodes='yes', show_nodetags= 'yes', show_eletags= 'yes')

#cargas
tagSerie, tagPattern= 1,1
ops.timeSeries('Linear',tagSerie)
ops.pattern('Plain',tagPattern,tagSerie)

# Cargas aplicadas en la armadura, ops.load(ID nodo, Fx, Fy)
ops.load(3,60,-120)

# Se definen registros de salida
ops.recorder('Element','-xml','FuerzasElementos.txt','-time','-ele',1,2,3,4,5,'axialForce')
ops.recorder('Node','-file','Reacciones.txt','-node',1,4,'-dof',1,2,'reaction')


# Se definen los parámetros del análisis estático.
ops.system('BandGeneral')
ops.numberer('RCM')
ops.constraints('Plain')
ops.test('NormDispIncr', 1.0e-6, 10)
ops.integrator('LoadControl', 0.1)
ops.algorithm('Newton')
ops.analysis('Static')
ops.analyze(10)

ops.wipe()

vfo.plot_deformedshape(model= 'armp02', loadcase='Estatico', scale=100)

