//
// Created by redra on 01.06.18.
//

#ifndef TESTFSMCONEPTS_STATE_HPP
#define TESTFSMCONEPTS_STATE_HPP

#include <cassert>
#include <type_traits>
#include <string>
#include <vector>
#include <queue>
#include <memory>

#include "IEvent.hpp"

class IState : public std::enable_shared_from_this<IState> {
 public:
  IState(std::weak_ptr<IState> _parent);
  virtual ~IState() = 0;

  void start() {
    assert(!parent_.lock() && "Impossible to start child FSM separately from main FSM");
    if (!parent_.lock()) {
      entryFrom(nullptr, IEvent{/* Default event */});
    }
  }

  void processEvent(const IEvent & _ev) {
    processEvent(_ev, false);
  }

  /**
   * Get state name
   * @return State name of the state
   */
  virtual std::string getStateName() const {
    return boost::typeindex::type_id_runtime(*this).pretty_name();
  }

  /**
   * Get full state name
   * @return Full name of the state
   */
  virtual std::string getFullName() const final {
    std::string stateName;
    if (auto parentState = parent_.lock()) {
      stateName += parentState->getFullName();
      if (!stateName.empty()) {
        stateName = stateName + ":";
      }
    }
    stateName += "[" + getStateName() + "]";
    return stateName;
  }

 protected:
  virtual void entryFrom(std::shared_ptr<IState> _from,
                         const IEvent &_ev) = 0;

  virtual void exitTo(std::shared_ptr<IState> _to,
                      const IEvent &_ev) = 0;

  virtual bool handleEvent(const IEvent & _ev) {
    return false;
  }

  virtual void noTransition(const IEvent & _ev) {
  }

 private:
  bool processEvent(const IEvent & _ev, bool isParentCall) {
    bool isProcessed = false;
    std::shared_ptr<IState> parentState;
    if (!isParentCall && (parentState = parent_.lock())) {
      isProcessed = parentState->processEvent(_ev, false);
    } else if (!in_transaction_) {
      in_transaction_ = true;
      if (current_) {
        isProcessed = current_->processEvent(_ev, true);
      }
      if (!isProcessed) {
        isProcessed = handleEvent(_ev);
      }
      if (!isProcessed) {
        noTransition(_ev);
      }
      in_transaction_ = false;
    } else if (!parent_.lock()) {
      event_queue_.push(_ev);
    }

    if (!in_transaction_ && !parent_.lock()) {
      while (!event_queue_.empty()) {
        auto & event = event_queue_.front();
        event_queue_.pop();
        processEvent(event);
      }
    }
    return isProcessed;
  }

 protected:
  std::weak_ptr<IState> parent_;
  std::shared_ptr<IState> current_ = nullptr;
  std::vector<std::shared_ptr<IState>> child_states_;

 private:
  std::shared_ptr< IState > holder_ = std::shared_ptr< IState >(this, [](IState*) {
    // NOTE(redra): Nothing need to do. Just create holder for responses and broadcasts
  });

  bool in_transaction_ = false;
  std::queue<IEvent> event_queue_;
};

inline
IState::IState(std::weak_ptr<IState> _parent)
  : parent_(_parent) {
}

inline
IState::~IState() {
}

#endif //TESTFSMCONEPTS_STATE_HPP
