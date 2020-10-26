# -*- coding: utf-8 -*-
""" Split Pipe by distance.  """

__title__ = 'Pipe Split'
__author__ = 'André Rodrigues da Silva'

from rpw import revit, db
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button, CheckBox)

from Autodesk.Revit.DB import Transaction

from Autodesk.Revit.DB.Plumbing.PlumbingUtils import BreakCurve 
from rpw.db.xyz import XYZ

try:
	Tubos = db.Collector(of_category='OST_PipeCurves',is_not_type=True)
	TipoTubo = db.Collector(of_category='OST_PipeCurves',is_type=True)

	PipeTypes = []
	for i in range(0,len(Tubos)):
		PipeTypes.append(Tubos[i].Name)

	PipeTypes = list(dict.fromkeys(PipeTypes))
	PipeTypes = dict(zip(PipeTypes, PipeTypes))


	components = [Label('Select the pipe type:'),
				   ComboBox('PipeType', PipeTypes),
				   Label('Distance:'),
				   TextBox('distance', Text="3.0"),
				   Separator(),
				   Button('Select')]
	form = FlexForm('Pipe Split', components)
	form.show()

	TuboMaterial = form.values['PipeType']
	L = float(form.values['distance'])*3.28084

	TuboSelecionado = []
	for i in range(0,len(Tubos)):
		if(Tubos[i].Name == TuboMaterial):
			TuboSelecionado.append(Tubos[i])

	#Tubos com comprimento maior que o selecionado
	TuboSecionado3 = []

	for i in range(0,len(TuboSelecionado)):
		if(TuboSelecionado[i].Location.Curve.Length > L):
			TuboSecionado3.append(TuboSelecionado[i])

	points = []
	pointsAUX = []		
	for i in range(0,len(TuboSecionado3)):
		if((TuboSecionado3[i].Location.Curve.Length/L)>int(TuboSecionado3[i].Location.Curve.Length/L)):
			t = int(TuboSecionado3[i].Location.Curve.Length/L) + 1
		else:
			t = int(TuboSecionado3[i].Location.Curve.Length/L)
		d = L *TuboSecionado3[i].Location.Curve.Direction
		for n in range(0,t):
			if(n ==0):
				continue
			else:
				pointsAUX.append(TuboSecionado3[i].Location.Curve.GetEndPoint(0) + n*d)
		points.append(pointsAUX)
		pointsAUX = []
		
	pipes = TuboSecionado3

	# Typical Transaction in Revit Python Shell / pyRevit
	doc = __revit__.ActiveUIDocument.Document
	transaction = Transaction(doc, 'Delete Object')
	transaction.Start()
	try:
		for t in range(0,len(pipes),1):
			for i in range(0,len(points[t]),1):	
				dbPoint = points[t][i]
				pipe = pipes[t]
				newPipeId = BreakCurve(doc, pipe.Id, dbPoint)
				newPipe = doc.GetElement(newPipeId)	
				newPipeConnectors = newPipe.ConnectorManager.Connectors
				connA = None
				connB = None
				for c in pipe.ConnectorManager.Connectors:
					pc = c.Origin
					nearest = [x for x in newPipeConnectors if pc.DistanceTo(x.Origin) < 0.01]
					if nearest:
						connA = c
						connB = nearest[0]
				takeoff = doc.Create.NewUnionFitting(connA, connB)	
	except:
		transaction.RollBack()
	else:
		transaction.Commit()

except:
	pass