EXECUTE_PROCESS(COMMAND ${CMAKE_COMMAND} -E compare_files ${SRC} ${DST} RESULT_VARIABLE result)
IF(result)
  EXECUTE_PROCESS(COMMAND ${CMAKE_COMMAND} -E copy ${SRC} ${DST})
ENDIF(result)
