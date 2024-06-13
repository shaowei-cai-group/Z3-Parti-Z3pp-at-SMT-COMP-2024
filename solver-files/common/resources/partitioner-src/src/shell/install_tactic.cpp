// Automatically generated file.
#include "tactic/tactic.h"
#include "cmd_context/tactic_cmds.h"
#include "cmd_context/cmd_context.h"
#include "math/subpaving/tactic/subpaving_tactic.h"
#include "tactic/arith/add_bounds_tactic.h"
#include "tactic/arith/card2bv_tactic.h"
#include "tactic/arith/degree_shift_tactic.h"
#include "tactic/arith/diff_neq_tactic.h"
#include "tactic/arith/eq2bv_tactic.h"
#include "tactic/arith/factor_tactic.h"
#include "tactic/arith/fix_dl_var_tactic.h"
#include "tactic/arith/fm_tactic.h"
#include "tactic/arith/lia2card_tactic.h"
#include "tactic/arith/lia2pb_tactic.h"
#include "tactic/arith/nla2bv_tactic.h"
#include "tactic/arith/normalize_bounds_tactic.h"
#include "tactic/arith/pb2bv_tactic.h"
#include "tactic/arith/probe_arith.h"
#include "tactic/arith/propagate_ineqs_tactic.h"
#include "tactic/arith/purify_arith_tactic.h"
#include "tactic/arith/recover_01_tactic.h"
#include "tactic/core/blast_term_ite_tactic.h"
#include "tactic/core/cofactor_term_ite_tactic.h"
#include "tactic/core/collect_statistics_tactic.h"
#include "tactic/core/ctx_simplify_tactic.h"
#include "tactic/core/der_tactic.h"
#include "tactic/core/distribute_forall_tactic.h"
#include "tactic/core/dom_simplify_tactic.h"
#include "tactic/core/elim_term_ite_tactic.h"
#include "tactic/core/elim_uncnstr2_tactic.h"
#include "tactic/core/elim_uncnstr_tactic.h"
#include "tactic/core/eliminate_predicates_tactic.h"
#include "tactic/core/euf_completion_tactic.h"
#include "tactic/core/injectivity_tactic.h"
#include "tactic/core/nnf_tactic.h"
#include "tactic/core/occf_tactic.h"
#include "tactic/core/pb_preprocess_tactic.h"
#include "tactic/core/propagate_values2_tactic.h"
#include "tactic/core/propagate_values_tactic.h"
#include "tactic/core/reduce_args_tactic.h"
#include "tactic/core/simplify_tactic.h"
#include "tactic/core/solve_eqs_tactic.h"
#include "tactic/core/special_relations_tactic.h"
#include "tactic/core/split_clause_tactic.h"
#include "tactic/core/symmetry_reduce_tactic.h"
#include "tactic/core/tseitin_cnf_tactic.h"
#include "tactic/portfolio/solver_subsumption_tactic.h"
#include "tactic/probe.h"
#include "tactic/tactic.h"
#define ADD_TACTIC_CMD(NAME, DESCR, CODE) ctx.insert(alloc(tactic_cmd, symbol(NAME), DESCR, [](ast_manager &m, const params_ref &p) { return CODE; }))
#define ADD_PROBE(NAME, DESCR, PROBE) ctx.insert(alloc(probe_info, symbol(NAME), DESCR, PROBE))
void install_tactics(tactic_manager & ctx) {
  ADD_TACTIC_CMD("subpaving", "tactic for testing subpaving module.", mk_subpaving_tactic(m, p));
  ADD_TACTIC_CMD("add-bounds", "add bounds to unbounded variables (under approximation).", mk_add_bounds_tactic(m, p));
  ADD_TACTIC_CMD("card2bv", "convert pseudo-boolean constraints to bit-vectors.", mk_card2bv_tactic(m, p));
  ADD_TACTIC_CMD("degree-shift", "try to reduce degree of polynomials (remark: :mul2power simplification is automatically applied).", mk_degree_shift_tactic(m, p));
  ADD_TACTIC_CMD("diff-neq", "specialized solver for integer arithmetic problems that contain only atoms of the form (<= k x) (<= x k) and (not (= (- x y) k)), where x and y are constants and k is a numeral, and all constants are bounded.", mk_diff_neq_tactic(m, p));
  ADD_TACTIC_CMD("eq2bv", "convert integer variables used as finite domain elements to bit-vectors.", mk_eq2bv_tactic(m));
  ADD_TACTIC_CMD("factor", "polynomial factorization.", mk_factor_tactic(m, p));
  ADD_TACTIC_CMD("fix-dl-var", "if goal is in the difference logic fragment, then fix the variable with the most number of occurrences at 0.", mk_fix_dl_var_tactic(m, p));
  ADD_TACTIC_CMD("fm", "eliminate variables using fourier-motzkin elimination.", mk_fm_tactic(m, p));
  ADD_TACTIC_CMD("lia2card", "introduce cardinality constraints from 0-1 integer.", mk_lia2card_tactic(m, p));
  ADD_TACTIC_CMD("lia2pb", "convert bounded integer variables into a sequence of 0-1 variables.", mk_lia2pb_tactic(m, p));
  ADD_TACTIC_CMD("nla2bv", "convert a nonlinear arithmetic problem into a bit-vector problem, in most cases the resultant goal is an under approximation and is useul for finding models.", mk_nla2bv_tactic(m, p));
  ADD_TACTIC_CMD("normalize-bounds", "replace a variable x with lower bound k <= x with x' = x - k.", mk_normalize_bounds_tactic(m, p));
  ADD_TACTIC_CMD("pb2bv", "convert pseudo-boolean constraints to bit-vectors.", mk_pb2bv_tactic(m, p));
  ADD_TACTIC_CMD("propagate-ineqs", "propagate ineqs/bounds, remove subsumed inequalities.", mk_propagate_ineqs_tactic(m, p));
  ADD_TACTIC_CMD("purify-arith", "eliminate unnecessary operators: -, /, div, mod, rem, is-int, to-int, ^, root-objects.", mk_purify_arith_tactic(m, p));
  ADD_TACTIC_CMD("recover-01", "recover 0-1 variables hidden as Boolean variables.", mk_recover_01_tactic(m, p));
  ADD_TACTIC_CMD("blast-term-ite", "blast term if-then-else by hoisting them.", mk_blast_term_ite_tactic(m, p));
  ADD_TACTIC_CMD("cofactor-term-ite", "eliminate term if-the-else using cofactors.", mk_cofactor_term_ite_tactic(m, p));
  ADD_TACTIC_CMD("collect-statistics", "Collects various statistics.", mk_collect_statistics_tactic(m, p));
  ADD_TACTIC_CMD("ctx-simplify", "apply contextual simplification rules.", mk_ctx_simplify_tactic(m, p));
  ADD_TACTIC_CMD("der", "destructive equality resolution.", mk_der_tactic(m));
  ADD_TACTIC_CMD("distribute-forall", "distribute forall over conjunctions.", mk_distribute_forall_tactic(m, p));
  ADD_TACTIC_CMD("dom-simplify", "apply dominator simplification rules.", mk_dom_simplify_tactic(m, p));
  ADD_TACTIC_CMD("elim-term-ite", "eliminate term if-then-else by adding fresh auxiliary declarations.", mk_elim_term_ite_tactic(m, p));
  ADD_TACTIC_CMD("elim-uncnstr2", "eliminate unconstrained variables.", mk_elim_uncnstr2_tactic(m, p));
  ADD_TACTIC_CMD("elim-uncnstr", "eliminate application containing unconstrained variables.", mk_elim_uncnstr_tactic(m, p));
  ADD_TACTIC_CMD("elim-predicates", "eliminate predicates, macros and implicit definitions.", mk_eliminate_predicates_tactic(m, p));
  ADD_TACTIC_CMD("euf-completion", "simplify using equalities.", mk_euf_completion_tactic(m, p));
  ADD_TACTIC_CMD("injectivity", "Identifies and applies injectivity axioms.", mk_injectivity_tactic(m, p));
  ADD_TACTIC_CMD("snf", "put goal in skolem normal form.", mk_snf_tactic(m, p));
  ADD_TACTIC_CMD("nnf", "put goal in negation normal form.", mk_nnf_tactic(m, p));
  ADD_TACTIC_CMD("occf", "put goal in one constraint per clause normal form (notes: fails if proof generation is enabled; only clauses are considered).", mk_occf_tactic(m, p));
  ADD_TACTIC_CMD("pb-preprocess", "pre-process pseudo-Boolean constraints a la Davis Putnam.", mk_pb_preprocess_tactic(m, p));
  ADD_TACTIC_CMD("propagate-values2", "propagate constants.", mk_propagate_values2_tactic(m, p));
  ADD_TACTIC_CMD("propagate-values", "propagate constants.", mk_propagate_values_tactic(m, p));
  ADD_TACTIC_CMD("reduce-args", "reduce the number of arguments of function applications, when for all occurrences of a function f the i-th is a value.", mk_reduce_args_tactic(m, p));
  ADD_TACTIC_CMD("reduce-args2", "reduce the number of arguments of function applications, when for all occurrences of a function f the i-th is a value.", mk_reduce_args_tactic2(m, p));
  ADD_TACTIC_CMD("simplify", "apply simplification rules.", mk_simplify_tactic(m, p));
  ADD_TACTIC_CMD("elim-and", "convert (and a b) into (not (or (not a) (not b))).", mk_elim_and_tactic(m, p));
  ADD_TACTIC_CMD("solve-eqs", "solve for variables.", mk_solve_eqs_tactic(m, p));
  ADD_TACTIC_CMD("special-relations", "detect and replace by special relations.", mk_special_relations_tactic(m, p));
  ADD_TACTIC_CMD("split-clause", "split a clause in many subgoals.", mk_split_clause_tactic(p));
  ADD_TACTIC_CMD("symmetry-reduce", "apply symmetry reduction.", mk_symmetry_reduce_tactic(m, p));
  ADD_TACTIC_CMD("tseitin-cnf", "convert goal into CNF using tseitin-like encoding (note: quantifiers are ignored).", mk_tseitin_cnf_tactic(m, p));
  ADD_TACTIC_CMD("tseitin-cnf-core", "convert goal into CNF using tseitin-like encoding (note: quantifiers are ignored). This tactic does not apply required simplifications to the input goal like the tseitin-cnf tactic.", mk_tseitin_cnf_core_tactic(m, p));
  ADD_TACTIC_CMD("solver-subsumption", "remove assertions that are subsumed.", mk_solver_subsumption_tactic(m, p));
  ADD_TACTIC_CMD("skip", "do nothing tactic.", mk_skip_tactic());
  ADD_TACTIC_CMD("fail", "always fail tactic.", mk_fail_tactic());
  ADD_TACTIC_CMD("fail-if-undecided", "fail if goal is undecided.", mk_fail_if_undecided_tactic());
  ADD_PROBE("is-unbounded", "true if the goal contains integer/real constants that do not have lower/upper bounds.", mk_is_unbounded_probe());
  ADD_PROBE("is-pb", "true if the goal is a pseudo-boolean problem.", mk_is_pb_probe());
  ADD_PROBE("arith-max-deg", "max polynomial total degree of an arithmetic atom.", mk_arith_max_degree_probe());
  ADD_PROBE("arith-avg-deg", "avg polynomial total degree of an arithmetic atom.", mk_arith_avg_degree_probe());
  ADD_PROBE("arith-max-bw", "max coefficient bit width.", mk_arith_max_bw_probe());
  ADD_PROBE("arith-avg-bw", "avg coefficient bit width.", mk_arith_avg_bw_probe());
  ADD_PROBE("is-qflia", "true if the goal is in QF_LIA.", mk_is_qflia_probe());
  ADD_PROBE("is-qfauflia", "true if the goal is in QF_AUFLIA.", mk_is_qfauflia_probe());
  ADD_PROBE("is-qflra", "true if the goal is in QF_LRA.", mk_is_qflra_probe());
  ADD_PROBE("is-qflira", "true if the goal is in QF_LIRA.", mk_is_qflira_probe());
  ADD_PROBE("is-ilp", "true if the goal is ILP.", mk_is_ilp_probe());
  ADD_PROBE("is-qfnia", "true if the goal is in QF_NIA (quantifier-free nonlinear integer arithmetic).", mk_is_qfnia_probe());
  ADD_PROBE("is-qfnra", "true if the goal is in QF_NRA (quantifier-free nonlinear real arithmetic).", mk_is_qfnra_probe());
  ADD_PROBE("is-nia", "true if the goal is in NIA (nonlinear integer arithmetic, formula may have quantifiers).", mk_is_nia_probe());
  ADD_PROBE("is-nra", "true if the goal is in NRA (nonlinear real arithmetic, formula may have quantifiers).", mk_is_nra_probe());
  ADD_PROBE("is-nira", "true if the goal is in NIRA (nonlinear integer and real arithmetic, formula may have quantifiers).", mk_is_nira_probe());
  ADD_PROBE("is-lia", "true if the goal is in LIA (linear integer arithmetic, formula may have quantifiers).", mk_is_lia_probe());
  ADD_PROBE("is-lra", "true if the goal is in LRA (linear real arithmetic, formula may have quantifiers).", mk_is_lra_probe());
  ADD_PROBE("is-lira", "true if the goal is in LIRA (linear integer and real arithmetic, formula may have quantifiers).", mk_is_lira_probe());
  ADD_PROBE("is-qfufnra", "true if the goal is QF_UFNRA (quantifier-free nonlinear real arithmetic with other theories).", mk_is_qfufnra_probe());
  ADD_PROBE("memory", "amount of used memory in megabytes.", mk_memory_probe());
  ADD_PROBE("depth", "depth of the input goal.", mk_depth_probe());
  ADD_PROBE("size", "number of assertions in the given goal.", mk_size_probe());
  ADD_PROBE("num-exprs", "number of expressions/terms in the given goal.", mk_num_exprs_probe());
  ADD_PROBE("num-consts", "number of non Boolean constants in the given goal.", mk_num_consts_probe());
  ADD_PROBE("num-bool-consts", "number of Boolean constants in the given goal.", mk_num_bool_consts_probe());
  ADD_PROBE("num-arith-consts", "number of arithmetic constants in the given goal.", mk_num_arith_consts_probe());
  ADD_PROBE("num-bv-consts", "number of bit-vector constants in the given goal.", mk_num_bv_consts_probe());
  ADD_PROBE("produce-proofs", "true if proof generation is enabled for the given goal.", mk_produce_proofs_probe());
  ADD_PROBE("produce-model", "true if model generation is enabled for the given goal.", mk_produce_models_probe());
  ADD_PROBE("produce-unsat-cores", "true if unsat-core generation is enabled for the given goal.", mk_produce_unsat_cores_probe());
  ADD_PROBE("has-quantifiers", "true if the goal contains quantifiers.", mk_has_quantifier_probe());
  ADD_PROBE("has-patterns", "true if the goal contains quantifiers with patterns.", mk_has_pattern_probe());
  ADD_PROBE("is-propositional", "true if the goal is in propositional logic.", mk_is_propositional_probe());
  ADD_PROBE("is-qfbv", "true if the goal is in QF_BV.", mk_is_qfbv_probe());
  ADD_PROBE("is-qfaufbv", "true if the goal is in QF_AUFBV.", mk_is_qfaufbv_probe());
}
