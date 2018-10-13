//
// Created by redra on 03.06.18.
//

#ifndef TESTFSMCONEPTS_IEVENT_HPP
#define TESTFSMCONEPTS_IEVENT_HPP

#include <string>
#include <boost/type_index.hpp>

struct IEvent {
  virtual ~IEvent() {
  }

  virtual std::string getName() const {
    return boost::typeindex::type_id_runtime(*this).pretty_name();
  }
};

#endif //TESTFSMCONEPTS_IEVENT_HPP
