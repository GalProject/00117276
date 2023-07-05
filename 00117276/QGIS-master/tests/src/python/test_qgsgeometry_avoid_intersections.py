"""QGIS Unit tests for QgsGeometry avoid intersections functionality.

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
__author__ = 'Martin Dobias'
__date__ = '20/08/2012'
__copyright__ = 'Copyright 2012, The QGIS Project'

import qgis  # NOQA

from qgis.core import QgsFeature, QgsGeometry, QgsVectorLayer
from qgis.testing import start_app, unittest

feat_wkt = [
    "POLYGON((11564467.4556225873529911 1004058.0506714906077832,11574000.25562258623540401 1001788.33638577628880739,11573173.43113279156386852 993520.09148781711701304,11573092.36990830115973949 992709.47924291924573481,11572184.48419401608407497 986808.22210006206296384,11569460.82705115899443626 977275.42210006201639771,11570059.38887163810431957 972187.64662597852293402,11570368.71276544407010078 969558.39352863351814449,11567645.05562258698046207 962749.25067149056121707,11561743.79847973026335239 965472.9078143477672711,11562197.74133687280118465 972735.99352863349486142,11562651.68419401533901691 980453.02210006199311465,11562197.74133687280118465 991801.59352863347157836,11564467.4556225873529911 1004058.0506714906077832))",
    "POLYGON((11585348.82705115899443626 1001788.33638577628880739,11595335.56990830041468143 1000426.50781434774398804,11598967.11276544444262981 994525.25067149056121707,11596726.68511567451059818 987803.96772218181286007,11594881.62705115787684917 982268.79352863342501223,11596210.5081571489572525 973631.06633969338145107,11596697.39847972989082336 970466.27924291917588562,11596243.4556225873529911 956847.99352863349486142,11589241.51456319727003574 957431.48861691600177437,11585348.82705115899443626 957755.87924291915260255,11583079.11276544444262981 965472.9078143477672711,11584503.3406173400580883 970315.28251079504843801,11585348.82705115899443626 973189.93638577638193965,11585802.76990830153226852 980906.96495720488019288,11585348.82705115899443626 991801.59352863347157836,11585348.82705115899443626 992546.05981434776913375,11585348.82705115899443626 999405.1363857762189582,11585348.82705115899443626 1001788.33638577628880739))",
    "POLYGON((11613039.34133687242865562 1000880.45067149063106626,11623026.08419401571154594 998156.79352863342501223,11623933.96990830078721046 992709.47924291924573481,11623927.13341948762536049 992620.60488835815340281,11623026.08419401571154594 980906.96495720488019288,11623933.96990830078721046 971828.10781434772070497,11624841.85562258772552013 956847.99352863349486142,11613493.28419401496648788 957301.93638577638193965,11612131.4556225873529911 963657.13638577633537352,11612131.4556225873529911 972258.57086853496730328,11612131.4556225873529911 973189.93638577638193965,11612131.4556225873529911 983176.67924291919916868,11611885.51540027372539043 988095.48368919338099658,11611677.51276544481515884 992255.53638577635865659,11612251.3477884866297245 995889.82486503885593265,11613039.34133687242865562 1000880.45067149063106626))",
    "POLYGON((11573173.43113279156386852 993520.09148781711701304,11576724.69587560556828976 993235.99030839197803289,11578337.0769300926476717 993106.99982403311878443,11579916.07919318228960037 992980.67964298592414707,11585348.82705115899443626 992546.05981434776913375,11585348.82705115899443626 991801.59352863347157836,11585802.76990830153226852 980906.96495720488019288,11585348.82705115899443626 973189.93638577638193965,11584503.3406173400580883 970315.28251079504843801,11577674.00869971700012684 971200.56627789419144392,11574530.55707954056560993 971608.05074717639945447,11570059.38887163810431957 972187.64662597852293402,11569460.82705115899443626 977275.42210006201639771,11572184.48419401608407497 986808.22210006206296384,11573092.36990830115973949 992709.47924291924573481,11573173.43113279156386852 993520.09148781711701304))",
    "POLYGON((11596726.68511567451059818 987803.96772218181286007,11602386.29350295476615429 987912.80634501413442194,11606709.58121678233146667 987995.94649335695430636,11611885.51540027372539043 988095.48368919338099658,11612131.4556225873529911 983176.67924291919916868,11612131.4556225873529911 973189.93638577638193965,11612131.4556225873529911 972258.57086853496730328,11605332.19643574021756649 972844.7139018839225173,11601876.97527708858251572 973142.57779487106017768,11596210.5081571489572525 973631.06633969338145107,11594881.62705115787684917 982268.79352863342501223,11596726.68511567451059818 987803.96772218181286007))",
    "MULTIPOLYGON(((11602386.29350295476615429 987912.80634501413442194,11602598.65562258660793304 994071.30781434779055417,11605393.122793298214674 993232.96766313433181494,11607138.08419401571154594 992709.47924291924573481,11606709.58121678233146667 987995.94649335695430636,11602386.29350295476615429 987912.80634501413442194)),((11605332.19643574021756649 972844.7139018839225173,11604868.36990830115973949 967742.62210006208624691,11603208.23603074997663498 967742.62210006208624691,11601690.76990830153226852 967742.62210006208624691,11601876.97527708858251572 973142.57779487106017768,11605332.19643574021756649 972844.7139018839225173)))",
    "MULTIPOLYGON(((11576724.69587560556828976 993235.99030839197803289,11577177.85562258772552013 997702.85067149065434933,11578957.31162258610129356 997448.64267149078659713,11580355.4556225873529911 997248.9078143477672711,11579916.07919318228960037 992980.67964298592414707,11578337.0769300926476717 993106.99982403311878443,11576724.69587560556828976 993235.99030839197803289)),((11577674.00869971700012684 971200.56627789419144392,11577177.85562258772552013 966380.79352863342501223,11574519.0474593210965395 966380.79352863342501223,11574000.25562258623540401 966380.79352863342501223,11574530.55707954056560993 971608.05074717639945447,11577674.00869971700012684 971200.56627789419144392)))"
]

newg_wkt = "POLYGON((11556863.91276544518768787 1008143.53638577624224126,11632785.85562258586287498 1005192.9078143477672711,11633693.74133687280118465 996794.96495720488019288,11605776.25562258809804916 996794.96495720488019288,11604300.94133687205612659 962862.73638577631209046,11602712.14133687317371368 962976.22210006194654852,11603620.0270511582493782 996794.96495720488019288,11588299.4556225873529911 997929.82210006203968078,11588753.39847972989082336 961160.45067149063106626,11575362.08419401571154594 961841.36495720490347594,11577745.28419401682913303 1000199.53638577624224126,11557658.3127654455602169 1001107.42210006201639771,11556863.91276544518768787 1008143.53638577624224126))"

"""
Correct result (three parts):
MULTIPOLYGON(((11556863.91276544518768787 1008143.53638577624224126,11632785.85562258586287498 1005192.9078143477672711,11633693.74133687280118465 996794.96495720488019288,11623253.05562258698046207 996794.96495720488019288,11623026.08419401571154594 998156.79352863342501223,11613039.34133687242865562 1000880.45067149063106626,11612394.26464514434337616 996794.96495720488019288,11605776.25562258809804916 996794.96495720488019288,11605618.44716152176260948 993165.37035266752354801,11605393.122793298214674 993232.96766313433181494,11603539.33281490206718445 993789.104656653245911,11603620.0270511582493782 996794.96495720488019288,11597281.42645414359867573 997264.49092735419981182,11595335.56990830041468143 1000426.50781434774398804,11585348.82705115899443626 1001788.33638577628880739,11585348.82705115899443626 999405.1363857762189582,11585348.82705115899443626 992546.05981434776913375,11579916.07919318228960037 992980.67964298592414707,11580355.4556225873529911 997248.9078143477672711,11578957.31162258610129356 997448.64267149078659713,11577586.53731508925557137 997644.46757256181444973,11577745.28419401682913303 1000199.53638577624224126,11573858.94101548381149769 1000375.19031474948860705,11574000.25562258623540401 1001788.33638577628880739,11564467.4556225873529911 1004058.0506714906077832,11563869.05927479639649391 1000826.71039342461153865,11557658.3127654455602169 1001107.42210006201639771,11556863.91276544518768787 1008143.53638577624224126)),((11604513.11028097197413445 967742.62210006208624691,11604300.94133687205612659 962862.73638577631209046,11602712.14133687317371368 962976.22210006194654852,11602840.09838385321199894 967742.62210006208624691,11603208.23603074997663498 967742.62210006208624691,11604513.11028097197413445 967742.62210006208624691)),((11584280.59107660688459873 961387.88155639520846307,11575362.08419401571154594 961841.36495720490347594,11575644.1196969747543335 966380.79352863342501223,11577177.85562258772552013 966380.79352863342501223,11577674.00869971700012684 971200.56627789419144392,11584503.3406173400580883 970315.28251079504843801,11583079.11276544444262981 965472.9078143477672711,11584280.59107660688459873 961387.88155639520846307)))

Incorrect result from QGIS < 2.2 (four parts):
MULTIPOLYGON(((11556863.91276544518768787 1008143.53638577624224126,11632785.85562258586287498 1005192.9078143477672711,11633693.74133687280118465 996794.96495720488019288,11623253.05562258698046207 996794.96495720488019288,11623026.08419401571154594 998156.79352863342501223,11613039.34133687242865562 1000880.45067149063106626,11612394.26464514434337616 996794.96495720488019288,11605776.25562258809804916 996794.96495720488019288,11605618.44716151989996433 993165.37035266763996333,11605393.122793298214674 993232.96766313433181494,11603539.33281490206718445 993789.104656653245911,11603620.0270511582493782 996794.96495720488019288,11597281.42645414359867573 997264.49092735419981182,11595335.56990830041468143 1000426.50781434774398804,11585348.82705115899443626 1001788.33638577628880739,11585348.82705115899443626 999405.1363857762189582,11585348.82705115899443626 992546.05981434776913375,11579916.07919318228960037 992980.67964298592414707,11580355.4556225873529911 997248.9078143477672711,11578957.31162258610129356 997448.64267149078659713,11577586.53731508925557137 997644.46757256181444973,11577745.28419401682913303 1000199.53638577624224126,11573858.94101548381149769 1000375.19031474948860705,11574000.25562258623540401 1001788.33638577628880739,11564467.4556225873529911 1004058.0506714906077832,11563869.05927479639649391 1000826.71039342461153865,11557658.3127654455602169 1001107.42210006201639771,11556863.91276544518768787 1008143.53638577624224126)),((11578337.0769300926476717 993106.99982403311878443,11577309.72997828386723995 993189.18758017767686397,11577309.72997828386723995 993189.18758017779327929,11578337.0769300926476717 993106.99982403311878443)),((11604513.11028097197413445 967742.62210006208624691,11604300.94133687205612659 962862.73638577631209046,11602712.14133687317371368 962976.22210006194654852,11602840.09838385321199894 967742.62210006208624691,11603208.23603074997663498 967742.62210006208624691,11604513.11028097197413445 967742.62210006208624691)),((11584503.3406173400580883 970315.28251079504843801,11583079.11276544444262981 965472.9078143477672711,11584280.59107660688459873 961387.88155639520846307,11575362.08419401571154594 961841.36495720490347594,11575644.1196969747543335 966380.79352863342501223,11577177.85562258772552013 966380.79352863342501223,11577674.00869971700012684 971200.56627789419144392,11584503.3406173400580883 970315.28251079504843801)))
"""

start_app()


class TestQgsGeometryAvoidIntersections(unittest.TestCase):

    def testNoSliverPolygons(self):

        # create a layer with some polygons that will be used as a source for "avoid intersections"
        l = QgsVectorLayer('MultiPolygon', 'test_layer', 'memory')
        assert l.isValid()

        features = []
        for i, wkt in enumerate(feat_wkt):
            f = QgsFeature(i + 1)
            f.setGeometry(QgsGeometry.fromWkt(wkt))
            features.append(f)

        l.dataProvider().addFeatures(features)
        assert l.featureCount() == 7

        # create a geometry and remove its intersections with other geometries

        g = QgsGeometry.fromWkt(newg_wkt)
        assert g.avoidIntersections([l]) == 2

        # the resulting multi-polygon must have exactly three parts
        # (in QGIS 2.0 it has one more tiny part that appears at the border between two of the original polygons)
        mpg = g.asMultiPolygon()
        assert len(mpg) == 3


if __name__ == '__main__':
    unittest.main()
