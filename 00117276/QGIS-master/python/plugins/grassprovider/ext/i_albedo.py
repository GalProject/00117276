"""
***************************************************************************
    i_albedo.py
    -----------
    Date                 : February 2016
    Copyright            : (C) 2016 by Médéric Ribreux
    Email                : medspx at medspx dot fr
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Médéric Ribreux'
__date__ = 'March 2016'
__copyright__ = '(C) 2016, Médéric Ribreux'

from .i import verifyRasterNum


def checkParameterValuesBeforeExecuting(alg, parameters, context):
    if alg.parameterAsBoolean(parameters, '-m', context):
        return verifyRasterNum(alg, parameters, context, 'input', 7)
    elif alg.parameterAsBoolean(parameters, '-n', context):
        return verifyRasterNum(alg, parameters, context, 'input', 2)
    elif (alg.parameterAsBoolean(parameters, '-l', context)
          or alg.parameterAsBoolean(parameters, '-a', context)):
        return verifyRasterNum(alg, parameters, context, 'input', 6)
    return True, None
