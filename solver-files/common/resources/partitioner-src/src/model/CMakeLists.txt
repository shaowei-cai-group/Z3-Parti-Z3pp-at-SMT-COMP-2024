z3_add_component(model
  SOURCES
    datatype_factory.cpp
    func_interp.cpp
    model2expr.cpp
    model_core.cpp
    model.cpp
    model_evaluator.cpp
    model_implicant.cpp
    model_macro_solver.cpp
    model_pp.cpp
    model_smt2_pp.cpp
    model_v2_pp.cpp
    numeral_factory.cpp
    struct_factory.cpp
    value_factory.cpp
  COMPONENT_DEPENDENCIES
    rewriter
    macros
  PYG_FILES
    model_evaluator_params.pyg
    model_params.pyg
)

