# -*- coding: utf-8 -*-
""" Remove elements duplicates."""

__title__ = 'Remove Duplicates'
__author__ = 'André Rodrigues da Silva'

from rpw import revit, db
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, TextBox,Separator, Button, CheckBox)
from rpw.db.xyz import XYZ

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

components = [Label('Select the categories:'),
				   CheckBox('Pipes', 'Pipes'),
                   CheckBox('PipeFitting', 'Pipe Fitting'),
                   CheckBox('PipeAccessory', 'Pipe Accessory'),
                   CheckBox('PlumbingFixtures', 'Plumbing Fixtures'),
                   CheckBox('Ducts', 'Ducts'),
                   CheckBox('DuctFitting', 'Duct Fitting'),
                   CheckBox('DuctAccessory', 'Duct Accessory'),
                   CheckBox('MechanicalEquipment', 'Mechanical Equipment'),
                   CheckBox('FlexPipe', 'FlexPipe'),
                   CheckBox('FlexDuct', 'FlexDuct'),
				   Separator(),
				   Button('Process')]
form = FlexForm('Remove Duplicates', components)
form.show()

tolerance_digits = 4

def get_point(elem):
            loc = elem.Location
            if loc is None:
                return None
            if isinstance(loc, LocationPoint):
                pt = loc.Point
                return (round(pt.X, tolerance_digits), round(pt.Y, tolerance_digits), round(pt.Z, tolerance_digits))
            return None


def round_point(pt, digits):
            """Round a 3D point to specified decimal places."""
            return (round(pt.X, digits), round(pt.Y, digits), round(pt.Z, digits))
            
            
if not form.values:
    pass #User closed the form window. Exiting script.
else:

    if form.values['Pipes']:
        # Collect all pipe elements (PipeCurves)
        pipes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PipeCurves) \
                                             .WhereElementIsNotElementType() \
                                             .ToElements()

        pipe_keys = []
        valid_pipes = []

        def get_pipe_key(pipe):
            """
            Generate a unique key for the pipe based on its start and end points.
            The key is order-independent (i.e., direction doesn't matter).
            """
            loc = pipe.Location
            if loc is None or not isinstance(loc, LocationCurve):
                return None
            curve = loc.Curve
            pt1 = round_point(curve.GetEndPoint(0), tolerance_digits)
            pt2 = round_point(curve.GetEndPoint(1), tolerance_digits)
            return tuple(sorted([pt1, pt2]))  # Order-insensitive key

        # Extract geometric keys from valid pipes
        for pipe in pipes:
            key = get_pipe_key(pipe)
            if key is not None:
                pipe_keys.append(key)
                valid_pipes.append(pipe)

        # Detect duplicates based on matching start and end points
        seen = set()
        duplicates_indices = []

        for i, key in enumerate(pipe_keys):
            if key in seen:
                duplicates_indices.append(i)
            else:
                seen.add(key)

        # Collect ElementIds of duplicate pipes
        pipes_to_delete = [valid_pipes[i].Id for i in duplicates_indices]

        # Start transaction to delete duplicate elements
        t = Transaction(doc, "Delete duplicate pipes (by start and end)")
        t.Start()

        for elem_id in pipes_to_delete:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass
        t.Commit()
        
        
    #########################################################################################################

    if form.values['Ducts']:
        # Collect all duct elements (PipeCurves)
        ducts = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctCurves) \
                                             .WhereElementIsNotElementType() \
                                             .ToElements()

        duct_keys = []
        valid_ducts = []

        def get_duct_key(duct):
            """
            Generate a unique key for the duct based on its start and end points.
            The key is order-independent (i.e., direction doesn't matter).
            """
            loc = duct.Location
            if loc is None or not isinstance(loc, LocationCurve):
                return None
            curve = loc.Curve
            pt1 = round_point(curve.GetEndPoint(0), tolerance_digits)
            pt2 = round_point(curve.GetEndPoint(1), tolerance_digits)
            return tuple(sorted([pt1, pt2]))  # Order-insensitive key

        # Extract geometric keys from valid ducts
        for duct in ducts:
            key = get_duct_key(duct)
            if key is not None:
                duct_keys.append(key)
                valid_ducts.append(duct)

        # Detect duplicates based on matching start and end points
        seen = set()
        duplicates_indices = []

        for i, key in enumerate(duct_keys):
            if key in seen:
                duplicates_indices.append(i)
            else:
                seen.add(key)

        # Collect ElementIds of duplicate ducts
        ducts_to_delete = [valid_ducts[i].Id for i in duplicates_indices]

        # Start transaction to delete duplicate elements
        t = Transaction(doc, "Delete duplicate ducts (by start and end)")
        t.Start()

        for elem_id in ducts_to_delete:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass
        t.Commit() 
        
        
    #########################################################################################################

    if form.values['FlexPipe']:
        # Collect all FlexPipe elements
        flex_pipes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_FlexPipeCurves) \
                                             .WhereElementIsNotElementType() \
                                             .ToElements()

        flex_pipe_keys = []
        valid_flex_pipes = []

        def get_flex_pipe_key(flex_pipe):
            """
            Generate a unique key for the flex_pipe based on its start and end points.
            The key is order-independent (i.e., direction doesn't matter).
            """
            loc = flex_pipe.Location
            if loc is None or not isinstance(loc, LocationCurve):
                return None
            curve = loc.Curve
            pt1 = round_point(curve.GetEndPoint(0), tolerance_digits)
            pt2 = round_point(curve.GetEndPoint(1), tolerance_digits)
            return tuple(sorted([pt1, pt2]))  # Order-insensitive key

        # Extract geometric keys from valid flex_pipes
        for flex_pipe in flex_pipes:
            key = get_flex_pipe_key(flex_pipe)
            if key is not None:
                flex_pipe_keys.append(key)
                valid_flex_pipes.append(flex_pipe)

        # Detect duplicates based on matching start and end points
        seen = set()
        duplicates_indices = []

        for i, key in enumerate(flex_pipe_keys):
            if key in seen:
                duplicates_indices.append(i)
            else:
                seen.add(key)

        # Collect ElementIds of duplicate flex_pipes
        flex_pipes_to_delete = [valid_flex_pipes[i].Id for i in duplicates_indices]

        # Start transaction to delete duplicate elements
        t = Transaction(doc, "Delete duplicate flex_pipes (by start and end)")
        t.Start()

        for elem_id in flex_pipes_to_delete:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass
        t.Commit() 
        
        
    #########################################################################################################

    if form.values['FlexDuct']:
        # Collect all FlexDuct elements
        flex_ducts = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_FlexDuctCurves) \
                                             .WhereElementIsNotElementType() \
                                             .ToElements()

        flex_duct_keys = []
        valid_flex_ducts = []

        def get_flex_duct_key(flex_duct):
            """
            Generate a unique key for the flex_duct based on its start and end points.
            The key is order-independent (i.e., direction doesn't matter).
            """
            loc = flex_duct.Location
            if loc is None or not isinstance(loc, LocationCurve):
                return None
            curve = loc.Curve
            pt1 = round_point(curve.GetEndPoint(0), tolerance_digits)
            pt2 = round_point(curve.GetEndPoint(1), tolerance_digits)
            return tuple(sorted([pt1, pt2]))  # Order-insensitive key

        # Extract geometric keys from valid flex_ducts
        for flex_duct in flex_ducts:
            key = get_flex_duct_key(flex_duct)
            if key is not None:
                flex_duct_keys.append(key)
                valid_flex_ducts.append(flex_duct)

        # Detect duplicates based on matching start and end points
        seen = set()
        duplicates_indices = []

        for i, key in enumerate(flex_duct_keys):
            if key in seen:
                duplicates_indices.append(i)
            else:
                seen.add(key)

        # Collect ElementIds of duplicate flex_ducts
        flex_ducts_to_delete = [valid_flex_ducts[i].Id for i in duplicates_indices]

        # Start transaction to delete duplicate elements
        t = Transaction(doc, "Delete duplicate flex_ducts (by start and end)")
        t.Start()

        for elem_id in flex_ducts_to_delete:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass
        t.Commit() 
        
        
    #########################################################################################################
       
    if form.values['PipeFitting']:
        Elements = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PipeFitting) \
                                     .WhereElementIsNotElementType() \
                                     .ToElements()

        Loc = []

        # Collect round positions
        for elem in Elements:
            pt = get_point(elem)
            if pt:
                Loc.append(pt)
            else:
                Loc.append(None)  # Ignore this elements

        # Find duplicate index
        views_elem = set()
        duplicates = []

        for i, val in enumerate(Loc):
            if val is None:
                continue
            if val in views_elem:
                duplicates.append(i)
            else:
                views_elem.add(val)

        # IDs of duplicate elements
        Elements_del = [Elements[i].Id for i in duplicates]


        t = Transaction(doc, "Delete duplicate elements")
        t.Start()

        for elem_id in Elements_del:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass

        t.Commit() 
        

    #########################################################################################################
       
    if form.values['PipeAccessory']:
        Elements = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PipeAccessory) \
                                     .WhereElementIsNotElementType() \
                                     .ToElements()

        Loc = []

        # Collect round positions
        for elem in Elements:
            pt = get_point(elem)
            if pt:
                Loc.append(pt)
            else:
                Loc.append(None)  # Ignore this elements

        # Find duplicate index
        views_elem = set()
        duplicates = []

        for i, val in enumerate(Loc):
            if val is None:
                continue
            if val in views_elem:
                duplicates.append(i)
            else:
                views_elem.add(val)

        # IDs of duplicate elements
        Elements_del = [Elements[i].Id for i in duplicates]


        t = Transaction(doc, "Delete duplicate elements")
        t.Start()

        for elem_id in Elements_del:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass

        t.Commit() 
        
    #########################################################################################################
       
    if form.values['PlumbingFixtures']:
        Elements = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_PlumbingFixtures) \
                                     .WhereElementIsNotElementType() \
                                     .ToElements()

        Loc = []

        # Collect round positions
        for elem in Elements:
            pt = get_point(elem)
            if pt:
                Loc.append(pt)
            else:
                Loc.append(None)  # Ignore this elements

        # Find duplicate index
        views_elem = set()
        duplicates = []

        for i, val in enumerate(Loc):
            if val is None:
                continue
            if val in views_elem:
                duplicates.append(i)
            else:
                views_elem.add(val)

        # IDs of duplicate elements
        Elements_del = [Elements[i].Id for i in duplicates]


        t = Transaction(doc, "Delete duplicate elements")
        t.Start()

        for elem_id in Elements_del:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass

        t.Commit() 


    #########################################################################################################
       
    if form.values['DuctFitting']:
        Elements = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctFitting) \
                                     .WhereElementIsNotElementType() \
                                     .ToElements()

        Loc = []

        # Collect round positions
        for elem in Elements:
            pt = get_point(elem)
            if pt:
                Loc.append(pt)
            else:
                Loc.append(None)  # Ignore this elements

        # Find duplicate index
        views_elem = set()
        duplicates = []

        for i, val in enumerate(Loc):
            if val is None:
                continue
            if val in views_elem:
                duplicates.append(i)
            else:
                views_elem.add(val)

        # IDs of duplicate elements
        Elements_del = [Elements[i].Id for i in duplicates]


        t = Transaction(doc, "Delete duplicate elements")
        t.Start()

        for elem_id in Elements_del:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass

        t.Commit() 



    #########################################################################################################
       
    if form.values['DuctAccessory']:
        Elements = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctAccessory) \
                                     .WhereElementIsNotElementType() \
                                     .ToElements()

        Loc = []


        # Collect round positions
        for elem in Elements:
            pt = get_point(elem)
            if pt:
                Loc.append(pt)
            else:
                Loc.append(None)  # Ignore this elements

        # Find duplicate index
        views_elem = set()
        duplicates = []

        for i, val in enumerate(Loc):
            if val is None:
                continue
            if val in views_elem:
                duplicates.append(i)
            else:
                views_elem.add(val)

        # IDs of duplicate elements
        Elements_del = [Elements[i].Id for i in duplicates]


        t = Transaction(doc, "Delete duplicate elements")
        t.Start()

        for elem_id in Elements_del:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass

        t.Commit() 



    #########################################################################################################
       
    if form.values['MechanicalEquipment']:
        Elements = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MechanicalEquipment) \
                                     .WhereElementIsNotElementType() \
                                     .ToElements()

        Loc = []

        # Collect round positions
        for elem in Elements:
            pt = get_point(elem)
            if pt:
                Loc.append(pt)
            else:
                Loc.append(None)  # Ignore this elements

        # Find duplicate index
        views_elem = set()
        duplicates = []

        for i, val in enumerate(Loc):
            if val is None:
                continue
            if val in views_elem:
                duplicates.append(i)
            else:
                views_elem.add(val)

        # IDs of duplicate elements
        Elements_del = [Elements[i].Id for i in duplicates]


        t = Transaction(doc, "Delete duplicate elements")
        t.Start()

        for elem_id in Elements_del:
            try:
                doc.Delete(elem_id)
            except Exception as e:
                pass

        t.Commit() 

    
        
    
    
