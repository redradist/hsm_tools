/**
 * @file .hpp
 * @date 14 Jun 2018
 * @brief It is an auto-generated file.
 * It example of template for CommonAPI Client.
 * This class is not ready for production use.
 * See project ICC: https://github.com/redradist/Inter-Component-Communication.git where it is more mature
 * @copyright Denis Kotov, MIT License. Open source: https://github.com/redradist/Inter-Component-Communication.git
 */

#ifndef _PCM_FSM_HPP_
#define _PCM_FSM_HPP_

#include <fsm/IState.hpp>

class PCM_FSM : public IState {
 public:
  static
  std::shared_ptr<IState> buildState(std::weak_ptr<IState> _parent = std::weak_ptr<IState>()) {
    return std::shared_ptr<PCM_FSM>(new PCM_FSM(_parent));
  }
  ~PCM_FSM();

  bool handleEvent(const IEvent & _ev) override;

  void entryFrom(std::shared_ptr<IState> _from,
                 const IEvent &_ev) override;

  void exitTo(std::shared_ptr<IState> _to,
              const IEvent &_ev) override;

 protected:
  PCM_FSM(std::weak_ptr<IState> _parent);
};

#endif  // _PCM_FSM_HPP_