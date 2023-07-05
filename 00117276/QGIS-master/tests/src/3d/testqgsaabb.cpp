/***************************************************************************
     testqgsaabb.cpp
     ----------------------
    Date                 : January 2023
    Copyright            : (C) 2023 by Stefanos Natsis
    Email                : uclaros at gmail dot com
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#include "qgstest.h"
#include "qgsaabb.h"

/**
 * \ingroup UnitTests
 * This is a unit test for the QgsAABB class
 */
class TestQgsAABB : public QObject
{
    Q_OBJECT
  public:
    TestQgsAABB() = default;

  private slots:
    void initTestCase();// will be called before the first testfunction is executed.
    void cleanupTestCase();// will be called after the last testfunction was executed.

    void testIsEmpty();

  private:
};

//runs before all tests
void TestQgsAABB::initTestCase()
{
}

//runs after all tests
void TestQgsAABB::cleanupTestCase()
{
}

void TestQgsAABB::testIsEmpty()
{
  // default constructor creates an empty AABB
  QgsAABB bbox = QgsAABB();
  QVERIFY( bbox.isEmpty() );

  // if any dimension extent is zero, AABB is empty
  bbox = QgsAABB( 0, 0, 0, 0, 1, 1 );
  QVERIFY( bbox.isEmpty() );

  bbox = QgsAABB( 0, 0, 0, 1, 0, 1 );
  QVERIFY( bbox.isEmpty() );

  bbox = QgsAABB( 0, 0, 0, 1, 1, 0 );
  QVERIFY( bbox.isEmpty() );

  // if no dimension extent is zero, AABB is not empty
  bbox = QgsAABB( 0, 0, 0, 1, 1, 1 );
  QVERIFY( !bbox.isEmpty() );
}

QGSTEST_MAIN( TestQgsAABB )
#include "testqgsaabb.moc"
