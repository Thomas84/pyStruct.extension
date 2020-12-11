from pyrevit import revit,DB


def formatter_square(unit):
    return u'{0}\xb2'.format(unit)

def formatter_cube(unit):
    return u'{0}\xb3'.format(unit)

def unit_from_type(display_unit_type):
    if display_unit_type == DB.DisplayUnitType.DUT_MILLIMETERS:
        return "mm" 
    elif display_unit_type == DB.DisplayUnitType.DUT_METERS:
        return "m"
    elif display_unit_type == DB.DisplayUnitType.DUT_CENTIMETERS:
        return "cm"
    elif display_unit_type == DB.DisplayUnitType.DUT_DECIMETERS:
        return "dm"
    elif display_unit_type == DB.DisplayUnitType.DUT_DECIMAL_FEET:
        return "decimal-feet"
    elif display_unit_type == DB.DisplayUnitType.DUT_FEET_FRACTIONAL_INCHES:
        return "feet-fractional inches"
    elif display_unit_type == DB.DisplayUnitType.DUT_FRACTIONAL_INCHES:
        return "fractional inches"
    elif display_unit_type == DB.DisplayUnitType.DUT_DECIMAL_INCHES:
        return "decimal-inches"
    elif display_unit_type == DB.DisplayUnitType.DUT_CUSTOM:
        return "custom"

    elif display_unit_type == DB.DisplayUnitType.DUT_SQUARE_FEET:
        return formatter_square("ft")   
    elif display_unit_type == DB.DisplayUnitType.DUT_SQUARE_INCHES:
        return formatter_square("in")  
    elif display_unit_type == DB.DisplayUnitType.DUT_SQUARE_METERS:
        return formatter_square("m")  
    elif display_unit_type == DB.DisplayUnitType.DUT_SQUARE_CENTIMETERS:
        return formatter_square("cm") 
    elif display_unit_type == DB.DisplayUnitType.DUT_SQUARE_MILLIMETERS:
        return formatter_square("mm") 
    elif display_unit_type == DB.DisplayUnitType.DUT_SQUARE_MILLIMETERS:
        return "acres"
    elif display_unit_type == DB.DisplayUnitType.DUT_SQUARE_MILLIMETERS:
        return "hectares"

    elif display_unit_type == DB.DisplayUnitType.DUT_CUBIC_FEET:
        return formatter_cube("ft")
    elif display_unit_type == DB.DisplayUnitType.DUT_CUBIC_METERS:
        return formatter_cube("m")
    elif display_unit_type == DB.DisplayUnitType.DUT_CUBIC_INCHES:
        return formatter_cube("in")
    elif display_unit_type == DB.DisplayUnitType.DUT_CUBIC_CENTIMETERS:
        return formatter_cube("cm")
    elif display_unit_type == DB.DisplayUnitType.DUT_CUBIC_MILLIMETERS:
        return formatter_cube("mm")
    elif display_unit_type == DB.DisplayUnitType.DUT_LITERS:
        return "litres"
    elif display_unit_type == DB.DisplayUnitType.DUT_GALLONS_US:
        return "US gallons"
    elif display_unit_type == DB.DisplayUnitType.DUT_CUBIC_YARDS:
        return formatter_cube("yd")
    elif display_unit_type == DB.DisplayUnitType.DUT_UNDEFINED:
        return "undefined"

def conv_unit_type(quant_type):
    if quant_type == "length":
        return DB.UnitType.UT_Length
    elif quant_type == "area":
        return DB.UnitType.UT_Area
    elif quant_type == "volume":
        return DB.UnitType.UT_Volume
        
def total(doc,unit_type,selection,builtin_enum):
    warning_count = 0 # warning fuse
    total_quant = 0.0

    for ele in selection:
        para = ele.Parameter[builtin_enum]
        if para:
            quant = para.AsDouble() # AsValueString() not recommended
            total_quant+=quant
        else:
            if warning_count < 10: # we don't wish to bomb the user
                forms.alert("Warning!!! {0} in the selection has no volume parameter".format(ele.Category.Name),
                        exitscript=False)
                warning_count+=1
    
    dut = para.DisplayUnitType
    total_quant = round(DB.UnitUtils.ConvertFromInternalUnits(total_quant,para.DisplayUnitType),4)
    try:
        formatted_total_quant = str(total_quant) + " " + unit_from_type(dut)
    except: # for none case
        formatted_total_quant = str(total_quant)

    # above three lines & function "unit_from_type" can be replaced with follwing two lines if unit symbol is turned on
    # units = doc.GetUnits()
    # formatted_total_quant = DB.UnitFormatUtils.Format(units, conv_unit_type(unit_type), total_quant, False, False)

    return formatted_total_quant,warning_count

