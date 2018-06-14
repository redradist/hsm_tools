#ifndef _PCM_FSM_HPP_
#define _PCM_FSM_HPP_

#include <iostream>
#include "PCM_FSM.hpp"
#include "Inactive/InactiveExternalAttributesState.hpp"
#include "Inactive/Inactive.hpp"
#include "Active/ActiveExternalAttributesState.hpp"
#include "Active/Active.hpp"

#include "PCMEvents.hpp"

PCM_FSM::PCM_FSM(std::weak_ptr<IState> _parent)
    : IState(_parent) {
  // Below added all states
  {
    // Creation Inactive state
    auto inactiveState = std::make_shared<Inactive>(shared_from_this());
    child_states_.push_back(inactiveState);
  }
  {
    // Creation Active state
    auto activeState = std::make_shared<Active>(shared_from_this());
    child_states_.push_back(activeState);
  }
}

PCM_FSM::~PCM_FSM() {
}

void PCM_FSM::entryFrom(std::shared_ptr<IState> _from, const IEvent &_ev) {
  // Below added all states
  if (typeid(powerOn) == typeid(_ev)) {
    current_ = inactiveState;
    current_->entryFrom(_from, _ev);
  }
  else if (typeid(startOn) == typeid(_ev)) {Action(_ev);
    [&_ev]() mutable  ;
    current_ = inactiveState;
    current_->entryFrom(_from, _ev);
  } {
    current_ = inactiveState;
    current_->entryFrom(_from, _ev);
  }
}

void PCM_FSM::exitTo(std::shared_ptr<IState> _to, const IEvent &_ev) {
  // Below added all states
  {
    current_->exitTo(_to, _ev);
    current_ = nullptr;
  }
}

bool PCM_FSM::handleEvent(const IEvent & _ev) {
  // Below added all states
  if (typeid(powerOn) == typeid(_ev) && i{} > k{}(_ev)
  )
  {
    current_->exitTo(_to, _ev);
    current_ = nullptr;
  }return false;
}



#endif  // _PCM_FSM_HPP_