/**
 * @file .hpp
 * @date 14 Jun 2018
 * @brief It is an auto-generated file.
 * It example of template for CommonAPI Client.
 * This class is not ready for production use.
 * See project ICC: https://github.com/redradist/Inter-Component-Communication.git where it is more mature
 * @copyright Denis Kotov, MIT License. Open source: https://github.com/redradist/Inter-Component-Communication.git
 */

#ifndef _ACTIVE_HPP_
#define _ACTIVE_HPP_

#include <fsm/IState.hpp>

class Active : public IState {
 public:
  static
  std::shared_ptr<IState> buildState(std::weak_ptr<IState> _parent = std::weak_ptr<IState>()) {
    return std::shared_ptr<Active>(new Active(_parent));
  }
  ~Active();

  bool handleEvent(const IEvent & _ev) override;

  void entryFrom(std::shared_ptr<IState> _from,
                 const IEvent &_ev) override;

  void exitTo(std::shared_ptr<IState> _to,
              const IEvent &_ev) override;

 protected:
  Active(std::weak_ptr<IState> _parent);
};

#endif  // _ACTIVE_HPP_