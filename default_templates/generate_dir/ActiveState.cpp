#ifndef _ACTIVE_HPP_
#define _ACTIVE_HPP_

#include <iostream>
#include "Active.hpp"
#include "PCMEvents.hpp"

Active::Active(std::weak_ptr<IState> _parent)
    : IState(_parent) {
}

Active::~Active() {
}

void Active::entryFrom(std::shared_ptr<IState> _from, const IEvent &_ev) {
}

void Active::exitTo(std::shared_ptr<IState> _to, const IEvent &_ev) {
}

bool Active::handleEvent(const IEvent & _ev) {
  // Below added all statesreturn false;
}



#endif  // _ACTIVE_HPP_