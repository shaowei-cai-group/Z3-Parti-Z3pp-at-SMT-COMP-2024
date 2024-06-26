/*++
Copyright (c) 2012 Microsoft Corporation

Module Name:

    tactic_manager.h

Abstract:
    Collection of tactics & probes

Author:

    Leonardo (leonardo) 2012-03-06

Notes:

--*/
#pragma once

#include "cmd_context/tactic_cmds.h"
#include "util/dictionary.h"

class tactic_manager {
protected:
    dictionary<tactic_cmd*>  m_name2tactic;
    dictionary<probe_info*>  m_name2probe;
    ptr_vector<tactic_cmd>   m_tactics;
    ptr_vector<probe_info>   m_probes;
    void finalize_tactic_manager();
public:
    ~tactic_manager();

    void insert(tactic_cmd * c);
    void insert(probe_info * p);
    tactic_cmd * find_tactic_cmd(symbol const & s) const; 
    probe_info * find_probe(symbol const & s) const;

    unsigned num_tactics() const { return m_tactics.size(); }
    unsigned num_probes() const { return m_probes.size(); }
    tactic_cmd * get_tactic(unsigned i) const { return m_tactics[i]; }
    probe_info * get_probe(unsigned i) const { return m_probes[i]; }

    ptr_vector<tactic_cmd> const& tactics() const { return m_tactics; }
    ptr_vector<probe_info> const& probes() const { return m_probes; }
    
        
};




