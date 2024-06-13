// Automatically generated file.
#include "util/gparams.h"
#include "ast/normal_forms/nnf.h"
#include "ast/normal_forms/nnf_params.hpp"
#include "ast/pp_params.hpp"
#include "math/polynomial/algebraic_params.hpp"
#include "model/model_evaluator_params.hpp"
#include "model/model_params.hpp"
#include "params/arith_rewriter_params.hpp"
#include "params/array_rewriter_params.hpp"
#include "params/bool_rewriter_params.hpp"
#include "params/bv_rewriter_params.hpp"
#include "params/context_params.h"
#include "params/fpa2bv_rewriter_params.hpp"
#include "params/fpa_rewriter_params.hpp"
#include "params/pattern_inference_params_helper.hpp"
#include "params/poly_rewriter_params.hpp"
#include "params/rewriter_params.hpp"
#include "params/seq_rewriter_params.hpp"
#include "params/solver_params.hpp"
#include "params/tactic_params.hpp"
#include "parsers/util/parser_params.hpp"
#include "solver/combined_solver_params.hpp"
#include "util/env_params.h"
void gparams_register_modules() {
{ param_descrs d; context_params::collect_param_descrs(d); gparams::register_global(d); }
{ param_descrs d; env_params::collect_param_descrs(d); gparams::register_global(d); }
{ auto f = []() { auto* d = alloc(param_descrs); nnf::get_param_descrs(*d); return d; }; gparams::register_module("nnf", f); }
{ auto f = []() { auto* d = alloc(param_descrs); nnf_params::collect_param_descrs(*d); return d; }; gparams::register_module("nnf", f); }
{ auto f = []() { auto* d = alloc(param_descrs); pp_params::collect_param_descrs(*d); return d; }; gparams::register_module("pp", f); }
{ auto f = []() { auto* d = alloc(param_descrs); algebraic_params::collect_param_descrs(*d); return d; }; gparams::register_module("algebraic", f); }
{ auto f = []() { auto* d = alloc(param_descrs); model_evaluator_params::collect_param_descrs(*d); return d; }; gparams::register_module("model_evaluator", f); }
{ auto f = []() { auto* d = alloc(param_descrs); model_params::collect_param_descrs(*d); return d; }; gparams::register_module("model", f); }
{ auto f = []() { auto* d = alloc(param_descrs); arith_rewriter_params::collect_param_descrs(*d); return d; }; gparams::register_module("rewriter", f); }
{ auto f = []() { auto* d = alloc(param_descrs); array_rewriter_params::collect_param_descrs(*d); return d; }; gparams::register_module("rewriter", f); }
{ auto f = []() { auto* d = alloc(param_descrs); bool_rewriter_params::collect_param_descrs(*d); return d; }; gparams::register_module("rewriter", f); }
{ auto f = []() { auto* d = alloc(param_descrs); bv_rewriter_params::collect_param_descrs(*d); return d; }; gparams::register_module("rewriter", f); }
{ auto f = []() { auto* d = alloc(param_descrs); fpa2bv_rewriter_params::collect_param_descrs(*d); return d; }; gparams::register_module("rewriter", f); }
{ auto f = []() { auto* d = alloc(param_descrs); fpa_rewriter_params::collect_param_descrs(*d); return d; }; gparams::register_module("rewriter", f); }
{ auto f = []() { auto* d = alloc(param_descrs); pattern_inference_params_helper::collect_param_descrs(*d); return d; }; gparams::register_module("pi", f); }
{ auto f = []() { auto* d = alloc(param_descrs); poly_rewriter_params::collect_param_descrs(*d); return d; }; gparams::register_module("rewriter", f); }
{ auto f = []() { auto* d = alloc(param_descrs); rewriter_params::collect_param_descrs(*d); return d; }; gparams::register_module("rewriter", f); }
{ auto f = []() { auto* d = alloc(param_descrs); seq_rewriter_params::collect_param_descrs(*d); return d; }; gparams::register_module("rewriter", f); }
{ auto f = []() { auto* d = alloc(param_descrs); solver_params::collect_param_descrs(*d); return d; }; gparams::register_module("solver", f); }
{ auto f = []() { auto* d = alloc(param_descrs); tactic_params::collect_param_descrs(*d); return d; }; gparams::register_module("tactic", f); }
{ auto f = []() { auto* d = alloc(param_descrs); parser_params::collect_param_descrs(*d); return d; }; gparams::register_module("parser", f); }
{ auto f = []() { auto* d = alloc(param_descrs); combined_solver_params::collect_param_descrs(*d); return d; }; gparams::register_module("combined_solver", f); }
gparams::register_module_descr("nnf", "negation normal form");
gparams::register_module_descr("pp", "pretty printer");
gparams::register_module_descr("algebraic", "real algebraic number package. Non-default parameter settings are not supported");
gparams::register_module_descr("pi", "pattern inference (heuristics) for universal formulas (without annotation)");
gparams::register_module_descr("rewriter", "new formula simplification module used in the tactic framework, and new solvers");
gparams::register_module_descr("solver", "solver parameters");
gparams::register_module_descr("tactic", "tactic parameters");
gparams::register_module_descr("combined_solver", "combines two solvers: non-incremental (solver1) and incremental (solver2)");
}
