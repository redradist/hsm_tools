/**
 * @file .hpp
 * @date 14 Jun 2018
 * @brief It is an auto-generated file.
 * It example of template for CommonAPI Client.
 * This class is not ready for production use.
 * See project ICC: https://github.com/redradist/Inter-Component-Communication.git where it is more mature
 * @copyright Denis Kotov, MIT License. Open source: https://github.com/redradist/Inter-Component-Communication.git
 */

#ifndef _INACTIVE_HPP_
#define _INACTIVE_HPP_

#include <fsm/IState.hpp>

class Inactive : public IState {
 public:
  static
  std::shared_ptr<IState> buildState(std::weak_ptr<IState> _parent = std::weak_ptr<IState>()) {
    return std::shared_ptr<Inactive>(new Inactive(_parent));
  }
  ~Inactive();

  bool handleEvent(const IEvent & _ev) override;

  void entryFrom(std::shared_ptr<IState> _from,
                 const IEvent &_ev) override;

  void exitTo(std::shared_ptr<IState> _to,
              const IEvent &_ev) override;

 protected:
  Inactive(std::weak_ptr<IState> _parent);
};

#endif  // _INACTIVE_HPP_