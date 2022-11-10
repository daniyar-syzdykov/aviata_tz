import uuid
import sqlalchemy as sa
from sqlalchemy import select, update, delete, exists
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base, DBMixin


class SearchResult(Base, DBMixin):
    __tablename__ = 'search_results'

    id = sa.Column(sa.Integer(), primary_key=True, nullable=False)
    uuid = sa.Column(UUID(as_uuid=True),
                     postgres_required=True, default=uuid.uuid4)
    status = sa.Column(sa.Boolean(), postgres_required=True, default=False)
    details = relationship('SearchResultDetail')

    @property
    def search_id(self):
        return str(self.uuid)

    @classmethod
    async def get_by_search_id(cls, search_id, session):
        query = select(SearchResult).where(SearchResult.uuid == search_id).\
            options(joinedload(SearchResult.details))
        result = await SearchResult._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None

    async def _modify_field(self, obj, field, action, session):
        field = getattr(self, field)
        act = getattr(field, action)
        act(obj)
        session.add(self)
        try:
            await session.commit()
        except Exception as e:
            session.rollback()
            raise e
        else:
            return {'success': True}

    async def update_details(self, new_result, session):
        return await self._modify_field(new_result, 'details', 'append', session)


class SearchResultDetail(Base, DBMixin):
    __tablename__ = 'search_result_details'

    id = sa.Column(sa.Integer(), primary_key=True)
    search_result_id = sa.Column(
        sa.Integer(), sa.ForeignKey('search_results.id'))
    items = sa.Column(JSONB(), postgres_required=True, default=[])
    price = sa.Column(sa.Float())
    currency = sa.Column(sa.String())
