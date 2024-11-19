from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey

Base = declarative_base()

# Create model url
class Domain(Base):
    __tablename__ = "domain"

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(Text, nullable=False)
    date_last_scan = Column(DateTime)
    link = relationship("Link", back_populates="domain")
    large_link = relationship("LargeLink", back_populates="domain")
    file = relationship("File", back_populates="domain")

    def update_last_scan(self):
        date_time = datetime.today()
        self.date_last_scan = date_time

# Create model link
class Link(Base):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(Text, nullable=False)
    date_last_scan = Column(DateTime)
    date_discovery = Column(DateTime, nullable=False)
    disabled = Column(Boolean, nullable=False)
    tries = Column(Integer, nullable=False)
    large = Column(Boolean, nullable=False)
    idDomain = Column(Integer, ForeignKey('domain.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    domain = relationship("Domain", back_populates="link")
    link_hash = relationship("LinkHash", back_populates="link")

    def new_link(self, link_url):
        """
        Populate the new link with the respective values
        :param link_url:
        :return:
        """
        date_time = datetime.today()
        self.link = link_url
        self.date_discovery = date_time
        self.disabled = 0
        self.tries = 0
        self.large = 0
    def update_last_scan(self):
        """
        Update last scan date
        :param:
        :return:
        """
        date_time = datetime.today()
        self.date_last_scan = date_time

    def disable_link(self):
        """
        Disable the link
        :param:
        :return:
        """
        date_time = datetime.today()
        self.disabled = 1
        self.date_last_scan = date_time


    def add_tries(self):
        """
        add_tries to the object
        :return: 
        """
        self.tries += 1

# Create model LargeLink
class LargeLink(Base):
    __tablename__ = "large_link"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(Text, nullable=False)
    header = Column(Text)
    idDomain = Column(Integer, ForeignKey('domain.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    domain = relationship("Domain", back_populates="large_link")

# Create model file
class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    original_name = Column(Text, nullable=False)
    type_of_file = Column(String(50), nullable=False)
    date_of_discovery = Column(DateTime, nullable=False)
    link = Column(Text, nullable=False)
    idDomain = Column(Integer, ForeignKey('domain.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    domain = relationship("Domain", back_populates="file")

# Create model hash
class Hash(Base):
    __tablename__ = "hash"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash = Column(String(100), nullable=False)
    link_hash = relationship("LinkHash", back_populates="hash")


# Create model urlHash
class LinkHash(Base):
    __tablename__ = "link_hash"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    idLink = Column(Integer, ForeignKey('link.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    idHash = Column(Integer, ForeignKey('hash.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    link = relationship("Link", back_populates="link_hash")
    hash = relationship("Hash", back_populates="link_hash")

    # def add_new_hash_url(self, db, url, hash, new_url_hash):
    #     self.url = url
    #     self.hash = hash
    #     db.add(new_url_hash)
    #     db.commit()

