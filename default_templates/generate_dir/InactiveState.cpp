#ifndef _INACTIVE_HPP_
#define _INACTIVE_HPP_

#include <iostream>
#include "Inactive.hpp"
#include "PCMEvents.hpp"

Inactive::Inactive(std::weak_ptr<IState> _parent)
    : IState(_parent) {
}

Inactive::~Inactive() {
}

void Inactive::entryFrom(std::shared_ptr<IState> _from, const IEvent &_ev) {
}

void Inactive::exitTo(std::shared_ptr<IState> _to, const IEvent &_ev) {
}

bool Inactive::handleEvent(const IEvent & _ev) {
  // Below added all statesreturn false;
}



#endif  // _INACTIVE_HPP_